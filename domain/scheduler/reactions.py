# actions.py - Define custom actions for message responses. Some of these functions are filthy beasts that need to be refactored.
# -*- coding: utf-8 -*-
# @TODO: Better logging. Explain yourself.

import datetime
from datetime import datetime as dt
import json
import logging
import time
from typing import Any, Text, Dict, List, Union

from rasa_core_sdk import Action, Tracker
from rasa_core_sdk.events import SlotSet, FollowupAction
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction
#from rasa_core_sdk.events import UserUtteranceReverted

from lib.send_res import Send

try:
    from lib.ext import kronos as kr
except ImportError:
    from build.src import kronos as kr
try:
    import lib.ext.scheduler as sch
except ImportError:
    import build.src.scheduler as sch
try:
    import lib.ext.convo as chat
except ImportError:
    import build.src.convo as chat

from build.src import date_time


logger = logging.getLogger(__name__)


class ActionNSFW(Action):
    """ This activates NSFW which can be added to any (active) form as a slot, & mapped to your learned nsfw intent """

    def name(self):
        return "action_nsfw"

    def run(self, dispatcher, tracker, domain):

        slots = []
        slots.append(SlotSet("NSFW", True))
        # dispatcher.utter_template("utter_suggest_color", tracker)
        #SlotSet("NSFW", 'yepp')
        message = 'Something you said was reported as NSFW.'
        dispatcher.utter_message(message)

        return slots


class ResetSlot(Action):
    """ The can be refactored as a factory with eval a/o get_attr """

    # Hard coded to reset a particular slot. :-/
    def name(self):
        return "action_reset_email"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("email", None)]


class ResetDate(Action):
    """ The can be refactored as a factory with eval a/o get_attr """

    # Hard coded to reset a particular slot. :-/
    def name(self):
        return "action_reset_date"

    def run(self, dispatcher, tracker, domain):
        slots = []
        slots.append(SlotSet('DATE', None))
        slots.append(SlotSet('Day', None))
        return slots
        #return [SlotSet("DATE", None)]

class ResetTime(Action):
    """ The can be refactored as a factory with eval a/o get_attr """

    # Hard coded to reset a particular slot. :-/
    def name(self):
        return "action_reset_time"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("Time", None)]



class ActionCheckDate(Action):

    def name(self):
        return "action_check_date"

    def run(self, dispatcher, tracker, domain):
        slots = []
        date_dirty = tracker.get_slot('month_and_date')  # CRF not used, slot not entity
        DATE = tracker.get_slot('DATE')  # Spacy NER fallback (pretrained)

        if date_dirty is not None:
            grok = kr.Grok()
            # returns list containing month and day parts, or None.
            date_clean = grok.clean_date_str(date_dirty)
        elif DATE is not None:
            grok = kr.Grok()
            # unlike clean_day, returns [month_name], [day] and not [month_no], [day]
            date_clean = grok.clean_date_str(DATE)
        else:
            return

        if date_clean is not None:  # If should be unnecessary.
            month_num, month_name = kr.month_name_and_num(date_clean[0])
            #slots.append(SlotSet('month_name', date_clean[0]))
            slots.append(SlotSet('date_month', month_num))
            slots.append(SlotSet('month_name', month_name))
            #slots.append(SlotSet('date_month', kr.get_int_from_month_name(date_clean[0])))
            slots.append(SlotSet('day_of_month', date_clean[1]))
            slots.append(
                SlotSet('day_ordinal', kr.ordinal_from_int(int(date_clean[1]))))
            # @TODO - Set ordinal for day/date
            # Spacy NER doesn't clean dates, so we use our NER which is *superior.*
            DATE = date_clean[0].capitalize() + ' ' + date_clean[1]
            slots.append(SlotSet('DATE', DATE))

        # clean_date_str() *should* return date in non-euro order, so this should not match.
        if date_clean[0].isnumeric():
            date = kr.get_date_from_month_and_day(date_clean)
        elif len(date_clean[0]) > 4:
            date = kr.get_date_from_month_name_and_day(date_clean)
        else:
            date = kr.get_date_from_month_abbr_and_day(date_clean)

        weekday = kr.get_weekday_from_date(date)
        slots.append(SlotSet('Day', weekday))

        msg = 'Let me quickly check my schedule for ' + weekday + ' ' + date_clean[0] + ' ' + date_clean[1]
        dispatcher.utter_message(msg)
        #time.sleep(10)

        # @TODO: Clean this up.
        when = {}
        day = str(date_clean[1])
        when['weekday'] = weekday
        when['month_name'] = month_name
        when['month'] = month_num
        when['day'] = day  # should be str not cast
        #when['ordinal_date'] = ''

        confirm, message = sch.check_date_avail(when)
        if confirm == 'yes':
            dispatcher.utter_message("Yes, " + message)
        elif confirm == 'no':
            # I can't believe you've done this.
            dispatcher.utter_message("Sorry, " + message)

        return slots


class ActionCheckDay(Action):
    # @TODO: confirm weekends. determine if it's "this friday" or "next friday"
    def name(self):
        return "action_check_day"

    # @when - dict containing date + time components.
    def validate(self, dispatcher, tracker, domain):
        try:
            return super().validate(dispatcher, tracker, domain)
        except Exception as e:
            print(e)
            # could not extract entity
            dispatcher.utter_message(
                "OMG I am so sorry, I really didn't get that \n"
                "What's a good day for you?")

            return []

    # #TODO: run method should just make call to app api. (API First)
    def run(self, dispatcher, tracker, domain):
        slots = []
        when = {}

        # This guard block is not needed if we override the validate() menthod.
        day_dirty = tracker.get_slot('Day')
        if day_dirty is None:
            day_dirty = tracker.get_slot('DATE')
            slots.append(SlotSet('Day', day_dirty))

        if day_dirty is None:
            dispatcher.utter_message(
                "Sorry, I didn't get that, what's a good day for you?")
            return [(ActionRepeat)]

        day_clean = kr.clean_day_str(day_dirty).capitalize()
        # kill this which is too polymorphous.
        day_clean = kr.day_abbr_to_full(day_clean)
        if day_dirty != day_clean:
            dispatcher.utter_message("Ok, " + day_clean)

        # full-on datetime obj w/ TZ
        if day_dirty != 'today':  # sub-optimal, move get_date_ function into clean_day_str
            when['date'] = kr.get_date_from_weekday(day_clean)
            ord_day = kr.ord_day_from_date(when['date'])
        elif day_dirty == 'today':
            when['date'] = kr.get_todays_date()
            ord_day = kr.ord_day_from_date(when['date'])

        # date here is month and day string?
        #ord_day = kr.ord_day_from_date(when['date'])
        #msg_lmc = 'By ' + day_clean + ' you mean ' + \
        #    str(when['date']) + ', right? Let me quickly check my schedule...'
        #dispatcher.utter_message(msg_lmc)
        #time.sleep(10)

        when = kr.get_date_parts(when)
        ymd = str(when['date']).split('-')
        when['date_year'] = ymd[0]
        when['month'] = ymd[1]
        when['ord'] = ord_day
        when['weekday'] = day_clean
        when['Day'] = day_clean.capitalize()  # not used
        month_name = kr.get_month_abbr_from_num(ymd[1])
        when['month_name'] = month_name

        slots.append(SlotSet('month_name', month_name))
        slots.append(SlotSet('date_month', ymd[1]))
        slots.append(SlotSet('day_of_month', ymd[2]))
        slots.append(SlotSet('day_ordinal', when['ord']))
        slots.append(SlotSet('date_year', ymd[0]))
        slots.append(SlotSet('Day', when['Day']))


        return slots


class ActionCheckDayConfirm(Action):
    # @TODO: confirm weekends. determine if it's "this friday" or "next friday"
    def name(self):
        return "action_check_day_confirm"

    # @when - dict containing date + time components.
    def validate(self, dispatcher, tracker, domain):
        try:
            return super().validate(dispatcher, tracker, domain)
        except Exception as e:
            print(e)
            # could not extract entity
            dispatcher.utter_message(
                "Sorry, I really didn't get that \n"
                "What's a good day for you?")

            return []

    # #TODO: run method should just make call to app api. (API First)
    def run(self, dispatcher, tracker, domain):
        slots = []
        when = {}

        # This guard block is not needed if we override the validate() menthod.
        day_dirty = tracker.get_slot('Day')
        if day_dirty is None:
            day_dirty = tracker.get_slot('DATE')
            slots.append(SlotSet('Day', day_dirty))

        if day_dirty is None:
            dispatcher.utter_message(
                "Sorry, I didn't get that, what's a good day for you?")
            return [(ActionRepeat)]

        day_clean = kr.clean_day_str(day_dirty).capitalize()
        # kill this which is too polymorphous.
        day_clean = kr.day_abbr_to_full(day_clean)
        if day_dirty != day_clean:
            dispatcher.utter_message("Ok, " + day_clean)

        # full-on datetime obj w/ TZ
        if day_dirty != 'today':  # sub-optimal, move get_date_ function into clean_day_str
            when['date'] = kr.get_date_from_weekday(day_clean)
            ord_day = kr.ord_day_from_date(when['date'])
        elif day_dirty == 'today':
            when['date'] = kr.get_todays_date()
            ord_day = kr.ord_day_from_date(when['date'])

        # date here is month and day string?
        #ord_day = kr.ord_day_from_date(when['date'])
        msg_lmc = 'By ' + day_clean + ' you mean ' + \
            str(when['date']) + ', right? Let me quickly check my schedule...'
        dispatcher.utter_message(msg_lmc)
        #time.sleep(10)

        when = kr.get_date_parts(when)
        ymd = str(when['date']).split('-')
        when['date_year'] = ymd[0]
        when['month'] = ymd[1]
        when['ord'] = ord_day
        when['weekday'] = day_clean
        when['Day'] = day_clean.capitalize()  # not used
        month_name = kr.get_month_abbr_from_num(ymd[1])
        when['month_name'] = month_name

        slots.append(SlotSet('month_name', month_name))
        slots.append(SlotSet('date_month', ymd[1]))
        slots.append(SlotSet('day_of_month', ymd[2]))
        slots.append(SlotSet('day_ordinal', when['ord']))
        slots.append(SlotSet('date_year', ymd[0]))
        slots.append(SlotSet('Day', when['Day']))

        confirm, message = sch.check_day_avail(when)
        if confirm == 'yes':
            dispatcher.utter_message("Yes, " + message)
        elif confirm == 'no':
            # I can't believe you've done this.
            dispatcher.utter_message("Sorry, " + message)

        return slots


class ActionCheckTime(Action):

    def name(self):
        return "action_check_time"

    def run(self, dispatcher, tracker, domain):
        slots = []
        when = {}

        if tracker.get_slot('Time') is not None and tracker.get_slot('Time').strip() != '':
            time_dirty = tracker.get_slot('Time')
        else:
            return slots
        if time_dirty is not None:  # redundant
            grok = kr.Grok()
            hr, min, ampm = grok.clean_time_str(time_dirty)

            time_clean = hr + ':' + min
            msg = 'Ok, checking my calendar to see if ' + time_clean + ' is free...'
            dispatcher.utter_message(msg)

            # I think there is a node.js module that does this.
            min = str(min)
            if min == '0':
                min = '00'

            slots.append(SlotSet('time_hour', hr))
            slots.append(SlotSet('time_minutes', min))
            slots.append(SlotSet('time_am_pm', ampm))

        # Convolutional Neuropathy
        when['month_name'] = tracker.get_slot('month_name')
        when['Day'] = tracker.get_slot('Day')
        if tracker.get_slot('day_ordinal') is not None:
            when['day'] = tracker.get_slot('day_ordinal')
        elif tracker.get_slot('day_of_month') is not None:
            when['day'] = tracker.get_slot('day_of_month')
        when['time_hour'] = hr
        when['time_minutes'] = min
        #if tracker.get_slot('time_am_pm') is not None:
        #    when['am_pm'] = tracker.get_slot('time_am_pm')
        if ampm is not None:
            when['am_pm'] = ampm  # ?

        confirm, message = sch.check_time_avail(when)

        if confirm == 'Yes':
            if tracker.get_slot('activity') is not None:
                activity = tracker.get_slot('activity')
            else:
                activity = 'do that'
            message = ", we can {} at {}:{} {} on {} {} {}".format(
                activity,
                when['time_hour'],
                when['time_minutes'],
                when['am_pm'],
                when['Day'],
                when['month_name'],
                when['day']
                )
            dispatcher.utter_message(confirm + message)
        elif confirm == 'no':
            # I can't believe you've done this.
            dispatcher.utter_message("Sorry, I have a conflict then, what's another time that works for you?")

        return slots

    @classmethod
    def checktime(cls, time_dirty, dispatcher, tracker):
        print('our class method')
        slots = []
        when = {}

        if time_dirty is not None:  # redundant
            grok = kr.Grok()
            hr, min, ampm = grok.clean_time_str(time_dirty)

            time_clean = hr + ':' + min
            msg = 'Ok, checking my calendar to see if ' + time_clean + ' is free...'
            dispatcher.utter_message(msg)

            # I think there is a node.js module that does this.
            min = str(min)
            if min == '0':
                min = '00'

            when = ActionDateParts.get_parts()

            when['time_hour'] = hr
            when['time_minutes'] = min
            when['time_am_pm'] = ampm

        # Convolutional Neuropathy
        when['month_name'] = tracker.get_slot('month_name')
        when['Day'] = tracker.get_slot('Day')
        if tracker.get_slot('day_ordinal') is not None:
            when['day'] = tracker.get_slot('day_ordinal')
        elif tracker.get_slot('day_of_month') is not None:
            when['day'] = tracker.get_slot('day_of_month')
        when['time_hour'] = hr
        when['time_minutes'] = min
        #if tracker.get_slot('time_am_pm') is not None:
        #    when['am_pm'] = tracker.get_slot('time_am_pm')
        if ampm is not None:
            when['am_pm'] = ampm  # ?

        """
        if cls.when['date'] is not None:
            cls.when['date'] = dt.strptime(cls.when['date'], '%Y-%m-%d')
            cls.when['weekday'] = cls.when['date'].strftime("%A")
            cls.when['month'] = cls.when['date'].strftime("%m")
            cls.when['day_of_month'] = cls.when['date'].strftime("%d")
            cls.when['ord'] = kr.ordinal_from_int(int(cls.when['day_of_month']))
            cls.when['date_year'] = cls.when['date'].strftime("%Y")
            cls.when['Day'] = cls.when['date'].strftime("%A")  # not used ?
            cls.when['month_name'] = cls.when['date'].strftime("%b")
        """
        when['Day'] = when['date'].strftime("%A")
        when['day'] = when['date'].strftime("%A")  # not used?
        when['month_name'] = when['date'].strftime("%b")

        confirm, message = sch.check_time_avail(when)

        if confirm == 'Yes':
            if tracker.get_slot('activity') is not None:
                activity = tracker.get_slot('activity')
            else:
                activity = 'do that'
            message = ", we can {} at {}:{} {} on {} {} {}".format(
                activity,
                when['time_hour'],
                when['time_minutes'],
                when['am_pm'],
                when['Day'],
                when['month_name'],
                when['ord']
                )
            dispatcher.utter_message(confirm + message)
        elif confirm == 'no':
            # I can't believe you've done this.
            dispatcher.utter_message("Sorry, I have a conflict then, what's another time that works for you?")

        return True


class ActionSendInvite(Action):  # Action Invite
    def name(self):
        return "action_send_invite"

    def run(self, dispatcher, tracker, domain):

        # Behold: Data inside a class method. And it's not PEP8!
        call = dict(
            activity=tracker.get_slot('activity'),  # Not curently used.
            month=tracker.get_slot('date_month'),
            month_name=tracker.get_slot('month_name'),
            day=int(tracker.get_slot('day_of_month')),
            weekday=tracker.get_slot('Day'),
            hour=int(tracker.get_slot('time_hour')),
            # we can't set int here bc of "00"
            mins=tracker.get_slot('time_minutes'),
            who=tracker.get_slot('nou'),
            email=tracker.get_slot('email'),
            ampm=tracker.get_slot('time_am_pm'),
            ord=kr.ordinal_from_int(int(tracker.get_slot('day_of_month')))
            )

        # Time is like, you never know what you'll get.
        if tracker.get_slot('date_month') is not None:
            call['month_no'] = int(tracker.get_slot('date_month'))
        elif tracker.get_slot('month_name') is not None:
            call['month_no'] = kr.get_int_from_month_name(
                tracker.get_slot('date_month'))
        if tracker.get_slot('time_am_pm') is not None:
            call['ampm'] = tracker.get_slot('time_am_pm')
        elif call['hour'] in range(1, 6):
            call['ampm'] = 'pm'
        elif call['hour'] in range(7, 12):
            call['ampm'] = 'am'
        else:
            call['ampm'] = ' '

        # Th ole off by double zero problem.
        if call['mins'] == '0':
            call['mins'] == '00'  # @FIXME: No longer needed.
        call['time'] = str(call['hour']) + " " + \
                           str(call['mins']) + " " + " EST"

        cal_date = datetime.date(2021, call['month_no'], call['day'])
        call_time = datetime.time(call['hour'], int(call['mins']))
        call['datetime'] = datetime.datetime.combine(cal_date, call_time)

        missing = sch.check_invite(call)
        if len(missing) < 1:
            sch.send_invite(call)
            response = "I just sent a calendar invitation to {0}. Please LMK if you don't get it!".format(call['email'])
            dispatcher.utter_message(response)
        elif len(missing) > 0:
            dispatcher.utter_message(
                "Sorry, I still need to get some information from you.")

        return []


class ActionSendRes(Action):
    def name(self):
        return "action_send_res"

    # @TODO: Template boilerplate, account credentials
    def run(self, dispatcher, tracker, domain):
        send = Send()
        sendres = {}
        res=tracker.get_slot('res')
        if tracker.get_slot('nou') is not None:
            sendres['Name'] = tracker.get_slot('nou').capitalize() +','
        sendres['FM'] = "Forest Mars"
        sendres['From'] = "themarsgroup@gmail.com"
        sendres['To'] =  tracker.get_slot('email')

        if res == 'cv':
            sendres['Subject'] =  sendres['FM'] + "' Resumé"
            sender = Send()
            try:
                sender.send_email(sendres)
                dispatcher.utter_message("I just sent it to you. Please LMK if you don't get it.")
            except Exception as e:
                print("oopsie, ", e)

        if res == 'jd':
            kind = tracker.get_slot('kind')
            sendres['Subject'] =  kind + " Job Description"
            sender = Send()
            try:
                dispatcher.utter_message("Let's have a quick call to discuss.")
            except Exception as e:
                print("oopsie, ", e)

            else:
                print("No things left that can be sent.")

    #def submit(self, dispatcher, tracker, domain):
    #    pass


class ActionUpdateContacts(Action):
    def name(self):
        return "action_update_contacts"

    def run(self, dispatcher, tracker, domain):
        slots = []
        if tracker.get_slot('PERSON'):
            person = tracker.get_slot('PERSON')
        elif tracker.get_slot('nou'):
            name = tracker.get_slot('nou')
        if 'person' in locals() and 'name' not in locals(): # Python-speak for "if person and not name" #cringe
            name = person.split()[0]
            slots.append(SlotSet('nou', name))
        elif 'name' in locals() and 'person' not in locals(): # Srsly, it's just so dirty.
            person = name

        try:
            number = tracker.sender_id.replace('+1', '') # tracker.current_state()["sender_id"]
            if number.strip() != 'default':
                sch.update_contacts(person, number)
        except:
            print("Can't imagine.")

        return slots


class ActionConfirmEvent(Action):
    def name(self):
        return "action_confirm_event"

    def run(self, dispatcher, tracker, domain):
        slots = []
        slots.append(SlotSet('confirm_event', True))

        return slots


class EmailForm(FormAction):
    def name(self):
        return "email_form"

    @staticmethod
    def required_slots(tracker):
        return ["email"]

    def validate_email(self, val, dispatcher, tracker, domain):
        if tracker.get_slot('email') is not None:
            email = tracker.get_slot('email')
            email = email.strip()  # FIXME: bug in regex validation
            email = sch.email_tld(tracker.get_slot('email'))
            if sch.is_valid_email(email) == False:
                dispatcher.utter_message(
                    "Sorry, that doesn't seem to be a good email.\n")
                return None
                slots.append(SlotSet('email', ''))
            elif sch.is_valid_email(email) == True:
                return email

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        return []


class WhoForm(FormAction):
    def name(self):
        return "who_form"

    @staticmethod
    def required_slots(tracker):
        return ["nou"]

    def request_next_slot(self, dispatcher, tracker, domain):
        for slot in self.required_slots(tracker):

            if slot == 'nou':
                who = tracker.get_slot(slot)
                if who is None:
                    dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                    return [SlotSet('nou', None)]

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        nou = tracker.get_slot('nou')
        kwargs = {'nou': nou}
        dispatcher.utter_template('utter_nicetohearfromu', tracker, **kwargs)
        return []


class ActionPreprocessWhenForm(Action):
    """ Because forms have no preprocessors, lol. """

    def name(self):
        return "action_preprocess_when"

    def run(self, dispatcher, tracker, domain):
        #input('heloo running')
        slots = []
        date = tracker.get_slot('DATE')

        if date is not None:  # slot was set before form ran, so not validated.
            # The should probably be handled with BILOU
            # replace_ = lambda s, d: s if not d else mrep(s.replace(*d.popitem()), d)
            vague = ['anytime', 'any time', 'sometime', 'sometime']
            for v in vague:
                date = date.replace(v, '')

            if date.lower().strip() in ['this week', 'next week', 'this month', 'next month']:
                dispatcher.utter_message("Pre: We can set something up for " + date)
                slots.append(SlotSet('DATE', None))

        return slots


# @TODO: Move formatters out of reactions file into custom handler.
class WhenForm(FormAction):
    def name(self):
        return "when_form"

    @staticmethod
    def required_slots(tracker):
        #   input('wtf')
        return ['DATE','Time']

    def request_next_slot(self, dispatcher, tracker, domain):
        """ mainly for message (utter_ask) template formatters. """
        print('req_next_slot')
        intent = tracker.latest_message['intent'].get('name')
        if intent == 'nvrmnd':  # Command
            dispatcher.utter_message("ok")
            return self.deactivate()
        elif intent == 'lost_the_plot':  # Fast Fail
            dispatcher.utter_message("Sorry, I'll back up")
            return self.deactivate()

        # Positive Match
        schedule_something = ['ask_availability', 'suggest_availability', 'suggest_date', 'suggest_time', 'vague_when', 'when', 'lets_do']
        if intent not in schedule_something:
            return self.deactivate()

        for slot in self.required_slots(tracker):
            print('iterating slots')

            if slot == 'DATE':
                print('if date')
                day = tracker.get_slot('Day')
                date = tracker.get_slot(slot)
                if isinstance(date, list):
                    date = date[0]

                if day is not None and date is None:
                    date_from_day = self.clean_date(dispatcher, tracker, day)
                    when = ActionDateParts.set_parts(date_from_day)
                    slots = []
                    slots.append(SlotSet('DATE', day))
                    dispatcher.utter_message("So, What's a good time for you {0}?".format(day))

                    return slots

                # Preprocess vague/bad dates.
                if isinstance(date, str):
                    if date is not None and self.preprocess_vague_date(dispatcher, date) == True:
                        input('holy shit')
                        dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                        return None # [SlotSet(slot, None)]
                    vague = ['anytime', 'any time', 'sometime', 'sometime']
                    for v in vague:
                        date = date.replace(v, '')
                    if date.lower().strip() in ['this week', 'next week', 'this month', 'next month']:
                        dispatcher.utter_message("We can set something up for " + date)
                        #slots.append(SlotSet('DATE', None))

            if slot == 'Time':
                print('if time')
                time_of_day = tracker.get_slot('TOD')
                # Preprocess vague/bad dates.
                if time_of_day is not None:
                    ask = "What time in the " + time_of_day.replace('the ', '') + " is good for you?"
                    dispatcher.utter_message(ask)
                time = tracker.get_slot('Time')
                #if time is not None:
                #    time = self.validate_Time(time, dispatcher, tracker, domain)
                #print('it wasnt so why dont you')
                #if time is not None:
                #    slots = []
                #    slots.append(SlotSet('Time', time))

                #    return slots

            print('should we request ', slot)
            print(self._should_request_slot(tracker, slot))
            if self._should_request_slot(tracker, slot):
                kwargs = {}
                if slot == 'DATE':

                    dispatcher.utter_template("utter_ask_{}".format(slot), tracker, **kwargs)
                    date = next(tracker.get_latest_entity_values('DATE'), None)
                    date = tracker.get_slot('DATE')  # ???
                    if date is not None:
                        date = self.validate_DATE(True, dispatcher, tracker, domain)

                    return [SlotSet('DATE', date)]#

                if slot == 'Time':

                    # This is so painful it hurts. (Why can't date be validated when date slot is requested?)
                    date = tracker.get_slot('DATE')
                    if date is not None:
                        date = self.validate_DATE(True, dispatcher, tracker, domain)
                    time = tracker.get_slot('Time')

                    return [SlotSet(slot, time)]

    def clean_date(self, dispatcher, tracker, DATE):
        day_dirty = tracker.get_slot('Day')  # CRF NER outperforma Spacy NER

        # Our CRF works where spaCy NER fails (such as weekday abbreviations just for one example.)
        if day_dirty is not None:
            day_clean = kr.clean_day_str(day_dirty).capitalize()
            day_clean = kr.day_abbr_to_full(day_clean)

            if day_dirty.lower().strip() not in ['today', '']:  # sub-optimal, move get_date_ function into clean_day_str
                date_clean = kr.get_date_from_weekday(day_clean)
                #ord_day = kr.ord_day_from_date(when['date'])
            elif day_dirty.lower() == 'today':
                date_clean = kr.get_todays_date()
        else:  # Spacy NER is fallback, bc it doesn't perform as well as our CRF NER (IWBH.)
            input(DATE)
            try:
                date_clean = self.preprocess_day_or_date(dispatcher, tracker, DATE)
            except Exception as e:
                print(e)

        return date_clean.strftime("%Y-%m-%d")

    def preprocess_date(self, DATE): #  Is this being used?
        date_clean = self.day_or_date(DATE)

    def preprocess_day_or_date(self, dispatcher, tracker, DATE):
        if DATE.isalpha() and len(DATE.split()) == 1:  # We most assuredly have a day, not a date. (Execept when Spacy NER fails.)
            try:
                date_orig = tracker.get_slot('DATE')
                day_clean = kr.clean_day_str(DATE).capitalize()
                date = kr.get_date_from_weekday(day_clean)
                date_str = datetime.datetime.strftime(date, "%B %d")
            except Exception as e:
                print(e)
        else:
            grok = kr.Grok()
            date_clean = grok.clean_date_str(DATE) #  unlike clean_day, returns [month_name], [day] and not [month_no], [day]
            if date_clean[0].isnumeric():
                date = kr.get_date_from_month_and_day(date_clean)
            elif len(date_clean[0]) > 4:
                date = kr.get_date_from_month_name_and_day(date_clean)
            else:
                date = kr.get_date_from_month_abbr_and_day(date_clean)

        return date

    def preprocess_vague_date(self, dispatcher, DATE):
        vague_dates = ['this week', 'next week', 'this month', 'next month', 'the coming week', 'this coming week', 'the coming month', 'this coming month']
        vague_days = ['a day', 'a good day', 'a good time']  # English language dependent. :-/

        if DATE.lower().replace('sometime', '').replace('in ', '').strip() in vague_dates:

            dispatcher.utter_message("We could set something up for " + DATE)
            return True
        elif DATE.lower().strip() in vague_days:
            return True

    def validate_DATE(self, val, dispatcher, tracker, domain):
        print('validating date')
        intent = tracker.latest_message['intent'].get('name')
        if intent == 'nvrmnd':  # This doesn't need to be in 2 places.
            dispatcher.utter_message("What's the magic word?")
            return self.deactivate()

        day_dirty = tracker.get_slot('Day')  # CRF NER outperforms Spacy NER
        if day_dirty is not None:
            DATE = day_dirty
        else:
            #  DATE = val
            DATE = tracker.get_slot('DATE')  # Spacy NER fallback (pretrained)

        # Guard conditions should not be needed.
        if DATE == None:
            return None

        # More guards for spaCy's 🦆 typing. Should all be consolidated together in a preprocessor.
        if isinstance(DATE, str):
            date_list = []
            date_list+=[DATE] # bc Spacy sometimes gives you a string, sometimes a list.
        elif isinstance(DATE, list):
            date_list = DATE

        for DATE in date_list:
            if DATE is not None and DATE.strip() != '':
                if self.preprocess_vague_date(dispatcher, DATE) is True: # this can likely be removed, we check in request_next_slot()
                    #dispatcher.utter_message("")
                    continue
            date_clean = self.clean_date(dispatcher, tracker, DATE)
            if date_clean.strip() == '':
                [SlotSet("DATE", None)] # This is suspect.

            when = ActionDateParts.set_parts(date_clean)
            kwargs = {}
            kwargs.update({"Day": when['Day']})
            kwargs.update({"month_name": when['month_name']})
            kwargs.update({"day_of_month": when['day_of_month']})
            #if tracker.get_slot('Time') is None or tracker.get_slot('Time').strip() != '':
            if tracker.get_slot('Time') is None:
                dispatcher.utter_template("utter_ask_Time".format('Time'), tracker, **kwargs)

            return date_clean

        return None

    def validate_Time(self, val, dispatcher, tracker, domain):
        print("validating time")
        dispatcher.utter_message('val time')
        kwargs = {}
        when = ActionDateParts.get_parts()
        kwargs.update({"Day": when['Day']})
        kwargs.update({"month_name": when['month_name']})
        kwargs.update({"day_of_month": when['day_of_month']})
        time = tracker.get_slot('Time')

        if time is None or time.strip() == '':
            return None
        print('hod it do')
        #if ActionCheckTime.checktime(time, dispatcher, tracker) == True:
            #return time

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        print('please submit')

        slots = []
        DATE = tracker.get_slot('DATE')
        if isinstance(DATE, list):
            DATE = DATE[0] # spaCy NER sometomes returns a list with the entity repeated. This is brittle, obvi.

        when = ActionDateParts.get_parts()  # This should probably be a different class method.

        # This is to catch vague dates captured by NER outside the form action (since form only validate fields it captures itself, and has not concept of preprocessing.)
        if DATE is not None and DATE.strip() != '':
            if self.preprocess_vague_date(dispatcher, DATE) is not None: # This is less than ideal.
                slots.append(SlotSet('DATE', None))
            # We literally have to validate every field in a form on submit, bc the form isn't smart enough to validate them.
            else:
                date_clean = self.clean_date(dispatcher, tracker, DATE)
                slots.append(SlotSet('DATE', date_clean))

        #self.set_date(False) # Reset date memory. (This can be removed ??)

        slots.append(SlotSet('month_name', when['month_name']))
        slots.append(SlotSet('date_month', when['month']))
        slots.append(SlotSet('day_of_month', when['day_of_month']))
        slots.append(SlotSet('day_ordinal', when['ord']))
        slots.append(SlotSet('date_year', when['date_year']))
        slots.append(SlotSet('Day', when['Day']))

        return slots


class TimeForm(FormAction):
    def name(self):
        return "time_form"

    def __init__(self, asked=False):
        self.set_date(asked)

    def get_date(self):
        return self._date

    def set_date(self, value):
        self._date = value

    @staticmethod
    def required_slots(tracker):
        return ["Time"]


# B/c datetime functions not available on "FE"
class ActionDateParts(Action):
    """ Rather than cramming this into the submit handler; makes available to be used by other modules. """

    def name(self):
        return "action_date_parts"

    @classmethod
    def __init__(cls):
        cls.when = None

    @classmethod
    def get_parts(cls):
        if cls.when is not None:
            return cls.when

    @classmethod
    def set_parts(cls, date):
        cls.when = {}

        # @FIXME
        if isinstance(date, list):
            date = date[0]

        cls.when['date'] = kr.validate_date_str(date)

        # Quick win if we have a valid date string.
        if cls.when['date'] is not None:
            cls.when['date'] = dt.strptime(cls.when['date'], '%Y-%m-%d')
            cls.when['weekday'] = cls.when['date'].strftime("%A")
            cls.when['month'] = cls.when['date'].strftime("%m")
            cls.when['day_of_month'] = cls.when['date'].strftime("%d")
            cls.when['ord'] = kr.ordinal_from_int(int(cls.when['day_of_month']))
            cls.when['date_year'] = cls.when['date'].strftime("%Y")
            cls.when['Day'] = cls.when['date'].strftime("%A")  # not used ?
            cls.when['month_name'] = cls.when['date'].strftime("%b")

        return cls.when

        # Date parsing if we didn't get the quick win.
        if when['date'] is None:
            grok = kr.Grok()
            date_clean = grok.clean_date_str(date)  # (returns list containing month and day parts, or None)

            # Shouldn't all this be handled by date time parsing class?
            if date_clean[0].isnumeric():
                date = kr.get_date_from_month_and_day(date_clean)
            elif len(date_clean[0]) > 4:
                date = kr.get_date_from_month_name_and_day(date_clean)
            else:
                date = kr.get_date_from_month_abbr_and_day(date_clean)

            when['date'] = date
            when['weekday'] = when['date'].strftime("%A")
            when['month'] = when['date'].strftime("%m")
            when['day_of_month'] = when['date'].strftime("%d")
            when['ord'] = kr.ordinal_from_int(int(when['day_of_month']))
            when['date_year'] = when['date'].strftime("%Y")
            when['Day'] = when['date'].strftime("%A")  # not used ?
            when['month_name'] = when['date'].strftime("%b")




            slots.append(SlotSet('month_name', when['month_name']))
            slots.append(SlotSet('date_month', when['month']))
            slots.append(SlotSet('day_of_month', when['day_of_month']))
            slots.append(SlotSet('day_ordinal', when['ord']))
            slots.append(SlotSet('date_year', when['date_year']))
            slots.append(SlotSet('Day', when['Day']))

            #return [FollowupAction('action_listen')]
        #msg = ' Let me quickly check my schedule for ' + when['Day'] + ' ' + when['month_name'] + ' ' + when['ord'] + ' at ' + when['hour'] +':'+ when['minutes']
        #msg = ' Let me quickly check my schedule for ' + when['Day'] + ' ' + when['month_name'] + ' ' + when['ord']
        #dispatcher.utter_message(msg)

        return slots

    #def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:

        #return []


class ActionChat(Action):
    """ User inputs not matching an active domain are considered tangential conversation and handled as such. """

    def name(self):
        return "action_chat"

    def run(self, dispatcher, tracker, domain):

        slots = []
        user = (tracker.current_state())["sender_id"]
        message = tracker.latest_message['text'] # :-)
        response = chat.ask(user, message)
        dispatcher.utter_message(response)

        return slots


class ActionRepeat(Action):  # AKA "What was that again?"
    """ Repeats last thing bot said when the user asks (not sure why you would need this in threaded messaging apps, but not too horrible a feature for voice assistants.) """

    def name(self) -> Text:
        return "action_repeat"

    def run(self, dispatcher, tracker, domain):
        if len(tracker.events) >= 3:
            pass
            # dispatcher.utter_message(tracker.events[-3].get('text'))
            # return [UserUtteranceReverted()]


class ActionRepeatSomething(Action):

    def name(self):
        return "action_repeat_"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_ignore_count = 2
        count = 0
        tracker_list = []

        while user_ignore_count > 0:
            event = tracker.events[count].get('event')
            if event == 'user':
                user_ignore_count = user_ignore_count - 1
            if event == 'bot':
                tracker_list.append(tracker.events[count])
            count = count - 1

        i = len(tracker_list) - 1
        while i >= 0:
            data = tracker_list[i].get('data')
            if data:
                if "buttons" in data:
                    dispatcher.utter_message(text=tracker_list[i].get(
                        'text'), buttons=data["buttons"])
                else:
                    dispatcher.utter_message(text=tracker_list[i].get('text'))
            i -= 1

        return []


# intent= tracker.latest_message[‘intent’].get(‘name’)
# tracker.latest_message[‘entities’]
