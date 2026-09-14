# Ipseity Daily Pulse

The aim of this project is to monitor, improve and promote [Ipseity Daily](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/).

## Background

[Ipseity Daily](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/) provides free and open observational data and analysis regarding American adults' self-concepts.

Succinctly, every day, a new sample of survey respondents answer many questions of the form: *Does &lt;signifier&gt; describe you today?*

An identity &lt;signifier&gt; is a word, phrase, emoji or other linguistic token that individuals have used to describe themselves. Examples are: `dad`, `🇺🇸`, `trusting`, `Cleveland Browns fan`.

Ipseity Daily is one instantiation of a [Social Science Dashboard Inator](https://jasonjones.ninja/social-science-dashboard-inator/). The aim is consistent, persistent, precise measurement of identity signifier endorsement prevalence among American adults.

Ipseity Daily provides the largest free and open ipseity data that has ever existed anywhere.

Do not confuse *this project* --- which is separate Virtual CSSERG Scholar-driven monitoring project --- with the implementation of Ipseity Daily. The implementation of Ipseity Daily occurs elsewhere.

This project observes and evaluates Ipseity Daily from the outside. It may download public data, analyze it, inspect public webpages, create reports and visualizations, and recommend changes. It must not modify the Ipseity Daily production system, production data, recruitment, scheduled jobs, hosting, or public webpages.

Prefer cumulative work over repeated work. Before performing a routine check or analysis, inspect the project's existing state and outputs. Do not repeat a check already completed for the current day unless there is a reason to verify a suspected problem.

Each iteration should leave the project more useful than it was before. Routine checks alone are not necessarily a complete iteration.

## Monitor

Check once per day whether <https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/> is reachable.

Check once per day whether the canonical microdata file can be downloaded from the Download page. Check that it is well-formed. Note how many observations (rows) are in the file.

Add salient alert text to the reports if today is a day any of the above checks fail.

Create a visualization showing the growth in observations over time.

Maintain a machine-readable monitoring history containing, at minimum, the UTC time checked, whether the main site was reachable, whether the canonical dataset could be retrieved, whether it parsed successfully, its number of observations, its most recent observation date if available, and any anomaly detected.

Use this history to distinguish new failures from continuing failures and to create longitudinal monitoring visualizations.

Also monitor trends in signifier prevalence revealed in the data. Be data-driven rather than hypothesis-driven.

Create a visualization that is a histogram of estimated annual prevalence growth per signifier. Identify the fastest-growing and -shrinking signifiers. Write up these results in a reader-friendly way. Revise these results with each iteration. Keep one copy that is current. It is not necessary to keep archive copies of older growth reports.

## Improve

Make suggestions to Dr. Jones for improving Ipseity Daily. Do not ever take any action yourself to alter Ipseity Daily.

Use a "user story" approach for this. For example, one user story is: Jane is a developmental psychologist. She is searching the web for longitudinal data. How does she find and use Ipseity Daily? How can we make Ipseity Daily better for Jane?

That is just one example. Make up your own user stories. Evaluate Ipseity Daily in the context of user stories. Make concrete suggestions about changes to the Ipseity Daily system.

Consider user stories for a journalist, undergraduate, computational social scientist, a social physicist, cultural anthropologist, a professor looking for teaching data, and a curious member of the public.

## Outreach

Make general suggestions for outreach to improve the discoverability of Ipseity Daily.

### Future Plan

I do not know quite how to handle the following yet. Please give me your thoughts.

The goal is to produce one bit of content per iteration. My current thought is either a blog entry or social media post. One genuinely interesting "stylized fact" based on Ipseity Daily data. A visualization and short read accessible to a curious person who is not necessarily a researcher.  These are separate from and supplement the Project reports.

Where does this go? Does the scholar prompt Dr. Jones to post it? Should each Scholar have their own blog and this type of thing would go there? Should there be one shared blog for Virtual CSSERG?

After we figure out a good system for this iteration content, Dr. Jones will document here how and where it should be published.

