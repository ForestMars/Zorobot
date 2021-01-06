## intent:following_up
- i got your email
- i received your email
- i got your message
- i received your message
- thanks for the email
- returning your call
- forest i got your email can we schedule a call
- i got your email can we schedule a call
- hi i reeived your email
- sorry im just now getting back to you
- sorry for the delay in getting back to you
- hi [forest](forest) i received your email. whats a good time for a call

## intent:will_lyk
- will lyk
- i will lyk
- i'll lyk
- will let you know
- i will let you know
- will lyk [tomorrow](Day)
- will lyk by [tomorrow](Day)
- will let you know [tomorrow](Day)
- i will let you know by [tomorrow](Day)
- i will know [next week](When)
- i will let you know by [next week]((When))
- i should know [tomorrow](Day)
- i should know by [tomorrow](Day)
- i should know [next week](When)
- i should know by [next week](When)
- i will know [tomorrow](Day)
- i will know by [tomorrow](Day)
- i will know by [next week](When)


## intent:time_of_day
- [morning](TOD)
- [afternoon](TOD)
- [evening](TOD)
- how about [morning](TOD)
- hows [morning](TOD) look
- hows your [morning](TOD) look?
- hows your [afternoon](TOD) look?
- can we do [afternoon](TOD)
- [afternoon](TOD) is better for me
- how about [afternoon](TOD)
- whats better [morning](TOD) or [afternoon](TOD)
- whats better for you [morning](TOD) or [afternoon](TOD)
- is [morning](TOD) or [afternoon](TOD) better for you
- [morning](TOD) is much better for me
- i have more time in the [afternoon](TOD) look
- [morning](TOD) could work, depending on what time

## intent:ask_which_day
- which days good for you
- which day is good for you
- whats a good day for you
- what day works for you
- which day works for you
- what day is good for you
- whats your calendar like
- whats your calendar look like
- whats the best day for you
- what day is best for you
- is there a specific day thats good for you
- any particular day thats good for you
- any particular day thats better for you
- which is your best day
- which is the best day
- whats a good day
- whats a good day for you
- what day
- what day works
- what day works for you
- any particular day
- any pariticular day good
- what day are you thinking
- whats your best availability
- what day is best for you
- you tell me what day is good

## intent:change_day
- can we change the day
- can we do a different day

## intent:suggest_different_day
- can we do [tomorrow](Day) instead
- can we do [the day after tomorrow](Day) instead
- can we do [monday](Day) instead
- can we do [tuesday](Day) instead
- can we do [wednesday](Day) instead
- can we do [thursday](Day) instead
- can we do [friday](Day) instead
- does [monday](Day) work
- does [tuesday](Day) work
- does [wednesday](Day) work
- does [thursday](Day) work
- does [friday](Day) work
- does [monday](Day) work instead
- does [tuesday](Day) work instead
- does [wednesday](Day) work instead
- does [thursday](Day) work instead
- does [friday](Day) work instead
- i would prefer [tuesday](Day)
- rather can we do [wednesday](Day)
- i would rather we do [monday](Day)
- [thursday](Day) is better for me
- [friday](Day) is better for me
- can we chage it to [tomorrow](Day) instead
- can we change to [monday](Day)
- can we change to [tuesday](Day)
- are you able to do [wednesday](Day) instead
- how does [thursday](Day) work instead

## intent:change_date_or_time
- [day]([day_or_time)
- [date](date_or_time)
- [time](date_or_time)
- the [day](date_or_time)
- the [date](date_or_time)
- the [time](date_or_time)
- change [day](date_or_time)
- change [date](date_or_time)
- change [time](date_or_time)
- change the [day](date_or_time)
- change the [dat](date_or_time)
- change the [time](date_or_time)
- the [day](date_or_time) please
- the [dat](date_or_time) please
- the [time](date_or_time) please
- change the [day](date_or_time) please
- change the [dat](date_or_time) please
- change the [time](date_or_time) please
- can we change the [day](date_or_time)
- can we change the [date](date_or_time)
- can we change the [time](date_or_time)
- i need to change the [day](date_or_time)
- i need to change the [date](date_or_time)
- i need to change the [time](date_or_time)
- id like to change the [day](date_or_time)
- id like to change the [date](date_or_time)
- id like to change the [time](date_or_time)
- lets adjust the [day](date_or_time)
- lets adjust the [date](date_or_time)
- lets adjust the [time](date_or_time)
- can we do a different [day](date_or_time) instead
- can we do a different [date](date_or_time) instead
- the [day](date_or_time) is wrong
- the [date](date_or_time) is wrong
- the [time](date_or_time) is wrong
- the [day](date_or_time) is incorrect
- the [date](date_or_time) is incorrect
- the [time](date_or_time) is incorrect
- you got the [day](date_or_time) wrong
- you got the [date](date_or_time) wrong
- you got the [time](date_or_time) wrong


### ~~~~~~~~~~~~~~~~~~~~~~~~~ React to proposed date time

## intent:affirm_day
- [monday](Day) is good for me
- [tuesday](Day) is good for me
- [wednesday](Day) works for me
- [thursday](Day) could work
- sure [friday](Day) sounds good
- sure lets do that
- yes thats good
- that day is good
- ok great lets do that

## intent:affirm_time
- [10:00](Time) looks good
- [200](Time) sounds good
- [1000am](Time) looks good
- [2pm](Time) looks good
- [10:00](Time) looks good
- [200](Time) looks good
- [10:00](Time) is fine
- [200](Time) should be fine
- that time sounds good
- that time should be fine
- that time is just fine

## intent:confirm_day_and_time
- ok, [Wed](Day) at [10am](Time) it is
- got it [Thursday](Day) at [10:00](Time) it is
- great then well talk on [Tue](Day) at [3pm](Time)
- confirmed talk you at [10:30](Time) on [Tuesday](Day)
- [2:00 pm](Time) on [Monday](Day) confirmed
- that day and time are fine with me
- just added to my calendar [10:45](Time) on [Friday](Day)

## intent:reject_day_or_time
- no good
- thats no good for me
- ah thats no good for me
- i have a conflict then
- i have something then
- no can do
- ah no can do
- sorry cant
- whats your 2nd choice
- whats your second choice


### ~~~~~~~~~~~~~~~~~~~~ Confirm Call ~~~~~~~~~~~~~~~~~~~~

## intent:confirm_call
- ok we are confirmed for
- ok confirming for
- got it ill talk to you then
- ok i have it on my calendar
- we are confirmed for
- confirming our call on
- ok great ill call you then
- ok great ill look for your call
- ok then i will call you
- ok then i will you call you on Wednesday
- ok then i will you call you at 10:00
- ok then i will you call you on Wednesday
- ok then i will you call you at 10:00
- ok are we confirmed
- so are we confirmed
- ok so are we confirmed

## intent:ask_to_confirm_call
- can we confirm our call
- can we confirm our plan
- how do we confirm our call
- lets confirm our plan
- lets confirm our call
- ok just to confirm [when](Ask_when) is our call
- [when](Ask_when) is our call for
- [when](Ask_when) did we confirm for
- [what day](Ask_day) are we having our call
- [what day](Ask_day) did we say
- [what time](Ask_time) are we having our call
- [what time](Ask_time) did we say
- can you remind me [what day](Ask_day) we said
- can you remind me [what time](Ask_time) we said
- just to confirm [what day](Ask_day) did we say
- just to confirm [what time](Ask_time) did we say

## intent:what_time_did_we_say
- what time did we say
- what time did we just say
- what time did we just decide
- what time did we say again
- can you confirm the time
- can you confirm the time again
- lets re-confirm the time
- ok just to confirm what time


### ~~~~~~~~~~~~~~~~~~~~~ Contact Info ~~~~~~~~~~~~~~~~~~~~

## intent:best_number_is
- [(212) 555-1212](phone)
- [314-159-2653](phone)
- [589-793-2384](phone)
- [(643)383-2795](phone)
- its [(718) 281-8284](phone)
- my number is [(212) 123-1212](phone)
- my phone number is [478-273-2834](phone)
- my best number is [(212)555-1212](phone)
- my best phone number is [(212)555-1212](phone)
- best number to reach me [(212)555-1212](phone)
- best number to reach me at [(212)555-1212](phone)
- best number to reach me is [(212)555-1212](phone)
- best number to reach me at is [(212)555-1212](phone)
- the best number to reach me is [(212)555-1212](phone)
- the best number to reach me at is [(212)555-1212](phone)
- heres my phone number [(212)555-1212](phone)
- my number is [212-555-1212](phone)
- my phone number is [212-555-1212](phone)
- my best number is [212-555-1212](phone)
- my best phone number is [212-555-1212](phone)
- best number to reach me [212-555-1212](phone)
- best number to reach me at [212-555-1212](phone)
- best number to reach me is [212-555-1212](phone)
- best number to reach me at is [212-555-1212](phone)
- the best number to reach me is [212-555-1212](phone)
- the best number to reach me at is [212-555-1212](phone)
- heres my phone number [212-555-1212](phone)

## intent:best_email_is
- [elmo@aol](email)
- [otto@gmail](email)
- [thatgy@hotmail](email)
- [yang@yahoo](email)
- [oldtimer@aol](email)
- [clever.name@gmail](email)
- [yang@yahoo](email)
- [lisa@hotmail](email)
- [oldtimer@aol](email)
- [yeezie@hotmail](email)
- [ebnozn@abc.de](email)
- [theone@gmail](email)
- [macfanboi@icloud](email)
- [kotke@icloud](email)
- [hello@bugmen.com](email)
- [db@bowie.net](email)
- [maxwell@tworooms.net](email)
- [jcm@2rooms.net](email)
- [faraday@cage.org](email)
- [claude@shannon.com](email)
- [don@knuth.org](email)
- [benoit.mandelbroit@fractal.xyz](email)
- [edward@witten.org](email)
- [first.last@mydomain](email)
- its [madam@curie.us](email)
- its [me@me.me](email)
- you can email at [foo@gmail.com](email)
- please use [idontwanttosayitoldyouso@itoldyou.so](email)
- my email [thatguy@gmail.com](email)
- my email is [thatgirl@hotmail.com](email)
- heres my email [thatgirl@yahoo.com](email)
- best email for me is [thatguy@thatguy.com](email)
- best email for me is [thatgirl@thatgirl.com](email)
- best email to reach me is [best@yourethebest.com](email)
- best email to reach me at is [rathernotsay@protonmail.com](email)
- the best email to reach me at is [schwarzchild@protonradius.com](email)
- if you dont have my email its [Earnest@Rutherford.com](email)
- if you need my email its [mitochondria@protonpump.io](email)
- ok so my email is [niels@bohr.dk](email)
- ok so my best email is [erwin@schrödinger.at](email)
- heres my email in case you need it [louis@debroglie.fr](email)
- heres my email in case you dont have it [werner@heisenberg.de](email)

## intent:change_email
- wrong email
- thats the wrong email
- thats the wrong email address
- wrong email address
- can you change my email
- you got my email wrong
- i typed my email wrong
- i mistyped my email
- autocorrect messed up my email
- i messed up my email
- i need to change my email


### ~~~~~~~~ Call Logistics ~~~~~~~~

## intent:do_you_have_my_number
- do you have my number
- do you still have my number
- did i give you my number
- does my number show up
- do you have this number
- do you know my number
- do you need my number

## intent:do_you_have_my_email
- do you have my email
- do you still have my email
- did i give you my email
- do you know my email
- do you need my email
- do you know what my email is
- you have my email right
- you already have my email right
- i already gave you my email
- did i give you my email
- did i tell you my email
- lets make sure you have my best email
- do you need my email
- im pretty sure you have my email

## intent:should_i_call_you
- i should call you
- should i call you
- do you want me to call you
- you want i should call you
- am i calling you
- am i calling you or are you calling me
- whos calling who
- should i call you then
- you want i should call you
- would you prefer i call you
- who is calling who

## intent:will_you_call_me
- should i look for your call
- you will call me
- you will call me then
- will you be calling me
- you are calling me
- are you calling me
- are you going to call me
- are you going to be calling me
- should i expect your call
- so you are calling me
- you will be calling me then
- will you call me then
- are you going to call me
- are you calling me

## intent:whats_your_number
- whats your number
- whats the best number to call you on
- what number should i call you on
- what number should i use
- whats your phone number
- should i call you on this number
- should i call you on this number or a different one
- is it still the same number
- do you still have the same number
- do i have the right number for you
- whats the best number to use
- whats the best number for you
- whats the best number to call you on
- yes whats your number
- i dont have your number what is it

## intent:whats_your_email
- whats your email
- whats your best email
- what email should I use
- do you still have the same email
- is this your email
- is this still your email
- tell me your email again
- whats your email pls

## intent:ask_send_invite
- should i send an invite
- should I send you an invite
- do you want me to send an invite

## intent:ask_will_you_send_invite
- are you sending the invite
- are you going to send the invite
- are you going to send out the calendar invite
- do you want to send me an invite
- are you sending an invite
- do you want to send the invitation
- do you want to send the invitation
- will you send an invite
- will you send the calendar event
- will you add this to our calendars
- will you be sending out the invite
- will you be sending out a calendar invitation
- will Zoro be sending out a calendar invite
- is the calendar invite automated
- will this automatically send out a calendar event

## intent:who_will_send_invite
- am i sending the invitation or are you
- am i sending the invitation or will you
- are you sending out the invite or am i
- are you sending out the calendar invite or am  i
- are you sending out the calendar invitation or am  i
- do you want me to send the invite or are you going to
- do you want me to send the invite or are you going to send it
- do you want to send the invitation or should i
- should i send an invitation or will you
- should i send an invitation or are you going to
- who will send the calendar invite me or you
- who is sending out the invitation
- who is sending out the invitation you or me
- will you send the invitation or should i

## check_cal
- i have to check my calendar
- lemme check my calendar
- lemme check my calendar first
- let me check my calendar
- let me check my calendar and get back to you
- i need to check my calendar
- i will need to check my calendar first
- i will need to check my availability
- i will need to check my availability at that time

## intent:call_me_now
- call me now
- call i call you
- can i call you now
- can you talk
- can you talk now
- can you take a call
- can we talk
- can we hop on a call
- can we do a call now
- can you do a call now
- can you hop on a call now


### ~~~~~~~~~~~~~~~~~~~~ Call Logistics ~~~~~~~~~~~~~~~~~~~~

## intent:oot
- ill be OOT
- i will be OOT
- i will be out of town
- i will be out of town [then](When)
- i will be out of town [until then](When)
- im planning a trip
- im planning a trip [then](When)
- i wont be in town
- i wont be in town [then](When)
- i dont think ill be around
- i dont think ill be around [then](When)
- ill be gone
- ill be gone [then](When)
- i will be gone
- ill be away
- i will be away
- im going to be gone
- im going to be away
- im planning to be away that week
- im planning to be away that day
- im planning to be out of town then
- ill be away [on the 4th](When)
- ill be away [over the holidays](When)

## get_back_to_you
- i have to get back to you
- i will have to get back to you
- i will have to get back to you on that
- ill lyk
- i will lyk
- ill have to lyk
- i will have to let you know
- im gonna have to lyk
- im gonna have to let you know
- ill have to lyk
- ill have to let you know
- let me get back to you
- let me get back to you later
- let me get back to you on that
- let me get back to you later on that
- let me get back to you on that later


## intent:multi_intent
- Hi Forest, thank you for coming back to me and i would be keen to set up a call. Can you let me know what your availability is? Thanks, [Sarah](Nou)
- Hi Forest thank you for getting back to me. I would be interested in setting up a call. Thanks very much, [Ann](Nou)
- Hi Forest thank you for getting back to me. I would like to set up a call. Sincerely, [Bud](Nou)
- Hi Forest, it's [lana](Nou) did you get the resumes i snt over? Let me know what you think of these candidates please.
- Hi Forest thank you for getting back to me. I am interested in setting up a call. Sincerely, [Chuck](Nou)
- Forest, I appreciate your reply to my Linked in message. What's a good time for a call you you? Best, [Lance](Nou)
- Hello Forest, what's a good day for us to have a call? Best, [Trey](Nou)
- Hey Forest, did you get my email? Will you let me know your availability for a call? Best, [will](Nou)
- hi forest, thanks for getting back to me and id like to set up a call. will you let me know what a good day is for you? thanks, [William](Nou)
- hi forest, thanks for getting back to me can we set up a call? whats a good day for you? cheers, [will](Nou)
- hi forest this is [Bill](Nou) from the acme company. Do you have time for a call this week?
- forest, dan here from bci. whats your availability for a call this week?
- hi forest, i sent you some resumes and wanted to see whats a good time to discuss? LMK! Best, [chip](Nou)
- hi forest thank you for getting back to me and i would like to schedule a call. what is your availability this week? thanks, [pam](Nou)
- hi forest thank you for getting back to me and i would like to schedule a call. what is your availability this week or next? thanks, [mel](Nou)
- hi forest thank you for getting back to me, can we hop on a call. whats good for this week? thanks, [mel](Nou)
- hi forest, good to hear from you. can you let me know your availability for a call? thanks, [angie](Nou)
- hi forest, thank you for the email. (this is [james](Nou) btw) i would be interested to set up a call.
- hi forest, i received your email and i would be interested in setting up a call.
- hi forest this is [andy](Nou). do you have a time for a call this week? I have some interesting candidates for you.
- hi forest this is [therese](Nou), what's your availability like this week? I sent some candidates your way
- hi forest this is [tatiana](Nou). what's a good time for a call? I have some resumes to send your way.
- hi forest this is [kevin](Nou) did you get the resumes i sent over
- hi forest this is [igor](Nou) just checking in to see if you got the candidates I sent over
- hi forest, this is [chip](Nou) i sent you some resumes and wanted to see whats a good time to discuss? LMK!
- hi forest it's [pam](Nou) thank you for getting back to me and i would like to schedule a call. what is your availability this week? thanks!
- hi forest it's [mel](Nou) thank you for getting back to me and i would like to schedule a call. what is your availability this week or next? thanks
- hy forest it’s [roger](Nou) have you had a chance to look at those resumes i sent
- hey forest this is [andy](Nou) thank you for getting back to me, can we hop on a call. whats good for this week?
- hey forest this is [barry](Nou) got time for a call this week?
- hey  this is [cal](Nou) we spoke on the phone.
- hey forest its [dan](Nou) did you get a chance to look at the candidates i sent you
- hello forest its [eric](Nou) have you had a chance to review the candidates
- hello forest this is [felicia](Nou). did you get the candidates i sent over
- Hey Forest, Love to set up a call. [Freddie](Nou) Scope Personel
- hi forest this is [arlo](Nou) thank you for getting back to me, can we hop on a call. whats good for this week?
- hi forest this is [barbara](Nou) got time for a call this week?
- hi this is [rachel](Nou) we spoke on the phone.
- hi forest its [chris](Nou) did you get a chance to look at the candidates i sent you
- hi forest its [dale](Nou) have you had a chance to review the candidates
- hi forest this is [larry](Nou). did you get the candidates i sent over
- hi forest it's [don](Nou). just following up on my email
- hi forest it's [ron](Nou). i received your email and
- hi forest it's [chelsea](Nou). great talking to you
- hi forest this is [arlo](Nou), thank you for getting back to me, can we hop on a call. whats good for this week?
- hi forest this is [barbara](Nou), got time for a call this week?
- hi this is [rachel](Nou), we spoke on the phone.
- hi forest its [chris](Nou), did you get a chance to look at the candidates i sent you
- hi forest its [dale](Nou), have you had a chance to review the candidates
- hi forest this is [larry](Nou), did you get the candidates i sent over
- hi forest it's [don](Nou), just following up on my email
- hi forest it's [ron](Nou), i received your email and
- hi forest it's [chelsea](Nou), great talking to you
- Forest asked me to [schedule a call](activity). My phone is [212 505 1212](phone). [Doyne Farmer](Nou)
- Forest asked me to [schedule a call](activity). My email is [artfarmer@gmail.com](phone). [Art Farmer](Nou)
- hi forest gave me this number to [schedule a call](activity) with him.
- is this the right number to [schedule a call](activity) with forest
- is this the right number to [book a call](activity) with forest


## intent:ask_call_with_name
- Hi this is [Harry](Nou), can I please schedule a [a call](activity) with [Forest](forest)?
- Can you set up [a call](activity) with [Forest](forest) please? Thanks, this is [Phil](Nou)
- Hi [Forest](forest) it's [Raymond](Nou), can we set up [a call](activity) please?
- hi zoro, it's [chris](Nou) are you able to set up [a call](activity) with [forest](forest)
- can you please set up a call
- can you please schedule a call
- i would like to book a call



## intent:multi_intent_no_name
- hi forest i really appreciate your coming back to me and i am interested in setting up a call
- hi forest, thank you for getting back to me and i would be interested to set up a call.
- hi forest, thank you for getting back to me. i would be interested to set up a call.
- hi forest, thank you for getting back to me. i would be interested in setting up a call.
- hi forest, thank you for the email. i would be interested in setting up a call.
- forest asked me to text you to set up a time for he and I to have a call.
- forest asked me to text you to set up a time for he and I to have a call. please let me know when we can do that
- Forest asked me to text you to set up a time for he and I to have a call. Please let me know when we can do that. TY [Gene](NAME)
- forest said to ask you to set up a call
- forest said you could schedule a call for us
- forest said you would set up a call for us

## intent:greet_with_name
- hi forest this is [kyle](Nou)
- hey forest this is [adam](Nou)
- hi forest this is [mike](Nou)
- hi forest this is [chris](Nou)
- hello forest this is [dierdre](Nou)
- hi this is [bonnie](Nou)
- hey this is [clyde](Nou)
- hi this is [rick](Nou)
- hi this is [will](Nou)
- hello this is [penn](Nou)
- hiya, its [paula](Nou)
- forst its [quentin](Nou)
- hi forest its [roy](Nou)
- hi forest its [sara](Nou)
- hi forest its [tashika](Nou)
- forest it's [victoria](Nou)
- hi forest it's [wayne](Nou)
- hi forest it's [yoli](Nou)
- it's [rick](Nou) forest
- this is [greg](Nou) forest


### ~~~ Meta ~~~

## intent:backup
- we didnt pick a day
- we didnt pick a date
- we didnt pick a time
- you didn't hear me correctly
- None is wrong
- what does None mean
- what day is None
- what time is None

## intent:blame_autocorrect
- i blame siri
- siri messed that up
- oops bad siri
- siri got that wrong
- voice recognition fail
- autocorrect fail
- autocorrect disaster
- why does autocorrect get everything wrong

## intent:hi_forest
- hi forest
- hello forest
- hey forest
- heya forest
- hiya forest
- good morning forest
- good afternoon forest

## intent:whats_none
- none?  
- none none?
- whats none
- what is none
- whats none none
- what is none none
- whats (None None)
- what is (None None)
- huh? none?
