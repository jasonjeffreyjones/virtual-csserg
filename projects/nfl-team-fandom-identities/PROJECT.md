# NFL Team Fandom Identities

We will address a growing list of research questions about NFL Team Fandom with data from Ipseity Daily.

- RQ1: How `happy` are `Cleveland Browns fans` as compared to other reference groups?
- RQ2: How does every NFL team fandom rank on `happy` `sad` `healthy` and `voter`? (The larger intent is to rank on every possible co-occurring signfier.)
- RQ3: During the 2025 NFL season, how did the happiness of each NFL team vary week to week?

## Background

Use data from [Ipseity Daily](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/).
Approach this project with ipseological methods. Read [Ipseology - A new science of the self](https://jasonjones.ninja/ipseology-a-new-science-of-the-self-book/)
Use Dr. Jones' terms (e.g. identity signifier) consistently and precisely. Ask Dr. Jones questions as necessary; he invented and developed ipseology.
Of course, you may additionally use any and all other methods and techniques that will improve the results.

## RQ1 as First Step

Use risk ratios to answer: *How `happy` are `Cleveland Browns fans` as compared to other reference groups?*

Here is what I mean. Some signifiers "go together."  Some don’t.
Consider `sad` and `anxious`. Then consider `sad` and `happy`.
Among people who said YES to `sad` what percent said YES to `anxious`?
Compare to people who said NO to `sad`.
From previous data: Among people who said YES to sad what percent said YES to anxious? 85%
Compare to people who said NO to sad: 33%
Sad respondents were 2.58 times more likely to be anxious (compared to not-sad respondents).
Call this a risk ratio. Push back if that is not a risk ratio. Push back if you think there is a strictly better way to measure.

The first reference group is all those who explicitly answer NO to `Cleveland Browns fan'. There is a large imbalance between the sizes, but that is okay.
Most American adults are not Cleveland Browns fans, and the survey data reflects that.

Download the anonymous microdata described here: https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html
If you are not able to access the files through https://jasonjones.ninja, use the Zenodo mirror at <https://doi.org/10.5281/zenodo.16576327>
Make sure you understand it thoroughly before beginning analysis.
As you see fit, document the structure of the data files.
Here are some important things to note:

- Make use of hashed_respondent_id and obs_date so that you know when signifiers are co-endorsed by the same individual at the same time.
- Only a small subset of identity signifiers are presented to every respondent every day.
- Except for the few every-day every-respondent signifiers, the rest have a probabilistic chance of presentation that is in tiers and may change over time.

## RQ2 and Beyond

You may work on other research questions as well. But for now, RQ1 is the place to concentrate work.
