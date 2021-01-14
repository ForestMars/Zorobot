# actions.py - Define custom actions for message responses
# -*- coding: utf-8 -*-
# @TODO: Better logging.

import datetime
import json
from typing import Any, Text, Dict, List, Union

from rasa_core_sdk import Action, Tracker
from rasa_core_sdk.events import SlotSet
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


# Explain yourself.


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


class ActionCheckDate(Action):

    def name(self):
        return "action_check_date"

    def run(self, dispatcher, tracker, domain):
        slots = []
        date_dirty = tracker.get_slot('month_and_date')  # CRF
        DATE = tracker.get_slot('DATE')  # Spacy NER fallback (pretrained)

        if date_dirty:
            grok = kr.Grok()
            # returns list containing month and day parts, or None.
            date_clean = grok.clean_date_str(date_dirty)
        elif DATE:
            grok = kr.Grok()
            # unlike clean_day, returns [month_name], [day] and not [month_no], [day]
            date_clean = grok.clean_date_str(DATE)

        if date_clean is not None:
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

        msg = 'Let me quickly check my schedule for (the date)' + \
            weekday + ' ' + date_clean[0] + ' ' + date_clean[1]
        dispatcher.utter_message(msg)

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
            str(when['date']) + ', right? Let me quickly check my schedule... (for that day)'
        dispatcher.utter_message(msg_lmc)

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

        if tracker.get_slot('Time') is not None:
            time_dirty = tracker.get_slot('Time')
        if time_dirty is not None:
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


class ActionSendInvite(Action):  # Action Invite
    def name(self):
        return "action_send_invite"

    def run(self, dispatcher, tracker, domain):

        # Behold: Data inside a class method.
        call = dict(
            # Superseded by month_name, can be killed.
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

        # You never know what you'll get.
        if tracker.get_slot('date_month') is not None:
            call['month_no'] = int(tracker.get_slot('date_month'))
        elif tracker.get_slot('month_name') is not None:
            call['month_no'] = kr.get_int_from_month_name(
                tracker.get_slot('date_month'))
        if tracker.get_slot('time_am_pm') is not None:
            #input(tracker.get_slot('time_am_pm'))
            call['ampm'] = tracker.get_slot('time_am_pm')
            #input(tracker.get_slot('time_am_pm'))
        elif call['hour'] in range(1, 6):
            call['ampm'] = 'pm'
        elif call['hour'] in range(7, 12):
            call['ampm'] = 'am'
        else:
            call['ampm'] = ' '
        #input(call['ampm'])
        # Th ole off by double zero problem.
        if call['mins'] == '0':
            call['mins'] == '00'  # @FIXME: No longer needed.
        #call['time'] = str(call['hour']) + " " + str(call['mins']) + " " + call['ampm'] + " EST"
        call['time'] = str(call['hour']) + " " + \
                           str(call['mins']) + " " + " EST"

        cal_date = datetime.date(2020, call['month_no'], call['day'])
        call_time = datetime.time(call['hour'], int(call['mins']))
        call['datetime'] = datetime.datetime.combine(cal_date, call_time)
        #slots.append(SlotSet('datetime', call['datetime']))

        missing = sch.check_invite(call)
        if len(missing) < 1:
            sch.send_invite(call)
            response = "I just sent a calendar invitation to " + \
                call['email'] + " Please LMK if you don't get it!"
            dispatcher.utter_message(response)
        elif len(missing) > 0:
            dispatcher.utter_message(
                "Sorry, I still need to get some information from you.")

        return []

class ActionSendRes(Action):
    def name(self):
        return "action_send_res"

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

    def submit(self, dispatcher, tracker, domain):
        pass


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
                dispatcher.utter_message("Got it.\n")
                return email

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        return []


class WhoForm(FormAction):
    def name(self):
        return "who_form"

    @staticmethod
    def required_slots(tracker):
        return ["who"]

    def validate_email(self, val, dispatcher, tracker, domain):
        if tracker.get_slot('email') is not None:
            email = tracker.get_slot('email')
            email = email.strip()  # FIXME: bug in regex validation before refactoring this block.
            email = sch.email_tld(tracker.get_slot('email'))
            if sch.is_valid_email(email) == False:
                dispatcher.utter_message(
                    "Sorry, that doesn't seem to be a good email.\n")
                return None
                slots.append(SlotSet('email', ''))
            elif sch.is_valid_email(email) == True:
                dispatcher.utter_message("Got it.\n")
                return email

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        return []


# @TODO: Move form logic out of reactions file into custom handler.
class WhenForm(FormAction):
    def name(self):
        return "when_form"

    @staticmethod
    def required_slots(tracker):
        return ["DATE"]

    def preprocess_day_or_date(self, dispatcher, DATE):

        if DATE.isalpha() and len(DATE.split()) == 1:  # We most assuredly have a day, not a date.
            day_clean = kr.clean_day_str(DATE).capitalize()
            date = kr.get_date_from_weekday(day_clean)
            date_str = datetime.datetime.strftime(date, "%M %d")
            msg = 'By ' + day_clean + ' you mean ' + \
                date_str + ', right? Let me quickly check my schedule... (for that day)'
            dispatcher.utter_message(msg)
        else:
            grok = kr.Grok()
            # unlike clean_day, returns [month_name], [day] and not [month_no], [day]
            date_clean = grok.clean_date_str(DATE)
            if date_clean[0].isnumeric():
                date = kr.get_date_from_month_and_day(date_clean)
            elif len(date_clean[0]) > 4:
                date = kr.get_date_from_month_name_and_day(date_clean)
            else:
                date = kr.get_date_from_month_abbr_and_day(date_clean)

        return date.strftime("%Y-%m-%d")

    def preprocess_date(DATE):
        date_clean = self.day_or_date(DATE)

    def validate_DATE(self, val, dispatcher, tracker, domain):
        DATE = tracker.get_slot('DATE')  # Spacy NER fallback (pretrained)
        day_dirty = tracker.get_slot('Day')  # CRF is fallback only here, but not by design.

        if DATE is not None:
            date_clean = self.preprocess_day_or_date(dispatcher, DATE)

        # Sorry, can't fallback to NER if you want to use a form. hahaha. Remove this.
        elif day_dirty is not None:
            day_clean = kr.clean_day_str(day_dirty).capitalize()
            day_clean = kr.day_abbr_to_full(day_clean)
            #slots.append(SlotSet('Day', day_clean)) # Sorry, you can't do this either.  :-/
            if day_dirty.lower().strip() not in ['today', '']:  # sub-optimal, move get_date_ function into clean_day_str
                date_clean = kr.get_date_from_weekday(day_clean)
                ord_day = kr.ord_day_from_date(when['date'])
            elif day_dirty.lower() == 'today':
                when['date'] = kr.get_todays_date()
                ord_day = kr.ord_day_from_date(when['date'])

        if date_clean is not None:
            return date_clean


    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        return []


class ActionDateParts(Action):
    """ Sadly, you can't do this with NER with Rasa by design-- even though it's kindof a trivial to do in NER, and a much better architectural pattern.
        Ca. Back-to-Front Middlewares. """

    def name(self):
        return "action_date_parts"

    def run(self, dispatcher, tracker, domain):
        slots = []
        when = {}
        when['date'] = tracker.get_slot('DATE')
        when['date'] = datetime.datetime.strptime(when['date'], '%Y-%m-%d')

        #when = kr.get_date_parts(when)
        #ymd = str(when['date']).split('-')
        when['weekday'] = when['date'].strftime("%A")
        when['month'] = when['date'].strftime("%m")
        when['day_of_month'] = when['date'].strftime("%d")
        when['ord'] = kr.ordinal_from_int(int(when['day_of_month']))
        when['date_year'] = when['date'].strftime("%Y")
        when['Day'] = when['date'].strftime("%A")  # not used ?
        #month_name = kr.get_month_abbr_from_num(ymd[1])
        when['month_name'] = when['date'].strftime("%b")

        slots.append(SlotSet('month_name', when['month_name']))
        slots.append(SlotSet('date_month', when['month']))
        slots.append(SlotSet('day_of_month', when['day_of_month']))
        slots.append(SlotSet('day_ordinal', when['ord']))
        slots.append(SlotSet('date_year', when['date_year']))
        slots.append(SlotSet('Day', when['Day']))

        """
        if 'date_clean' in locals():
            dispatcher.utter_message(date_clean)
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
            """

        msg = 'FORM: Let me quickly check my schedule for (the date) ' + when['Day'] + ' ' + when['month_name'] + ' ' + when['ord']
        #weekday + ' ' + date_clean[0] + ' ' + date_clean[1]
        dispatcher.utter_message(msg)

        return slots # And yes, we can use DATE ???

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        # Unfortunately, submit *always* fires even if the form was previously completed. So, yeah, just write more custom code as a workaround, right?
        #name = tracker.get_slot('nou')
        #msg = "Nice to hear from you " + name
        #dispatcher.utter_message(msg)
        return []




class ActionChat(Action):
    """ User inputs not matching an active domain are considered general conversation and handled as such. """

    def name(self):
        return "action_chat"

    def run(self, dispatcher, tracker, domain):

        slots = []
        user = (tracker.current_state())["sender_id"]
        #input(tracker.latest_message)
        message = tracker.latest_message['text'] # :-)
        #dispatcher.utter_message(message)

        response = chat.ask(user, message)
        dispatcher.utter_message(response)

        return slots


class ActionRepeat(Action):
    """ Repeats last thing bot said when the user asks (not sure why you would need this in threaded messaging apps, but I guess it's not too horrible a feature for voice assistants.) """

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
