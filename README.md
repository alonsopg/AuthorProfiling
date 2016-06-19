# Author Profiling @ PAN-2015

[Our participation](http://ceur-ws.org/Vol-1391/72-CR.pdf) for the [author profiling task 2015](http://www.uni-weimar.de/medien/webis/events/pan-15/pan15-web/author-profiling.html). Authorship analysis deals with the classification of texts into classes based on the stylistic choices of their authors. Beyond the author identification and author verification tasks where the style of individual authors is examined, author profiling distinguishes between classes of authors studying their sociolect aspect, that is, how language is shared by people. This helps in identifying profiling aspects such as gender, age, native language, or personality type. Author profiling is a problem of growing importance in applications in forensics, security, and marketing. E.g., from a forensic linguistics perspective one would like being able to know the linguistic profile of the author of a harassing text message (language used by a certain type of people) and identify certain characteristics (language as evidence). Similarly, from a marketing viewpoint, companies may be interested in knowing, on the basis of the analysis of blogs and online product reviews, the demographics of people that like or dislike their products. The focus is on author profiling in social media since we are mainly interested in everyday language and how it reflects basic social and personality processes.

## Task

This task is about predicting an author's demographics from his writing. Participants will be provided with Twitter tweets in English and Spanish to predict age, gender and personality traits. Moreover, they will be provided also with tweets in Italian and Dutch and asked to predict the gender and personality. 

## About

We present our approach to extract profile information from anonymized tweets for the author profiling task at PAN 2015. Particularly we explore the versatility of random forest classifiers for the genre and age groups information and random forest regressions to  score important aspects of the personality of a user. Furthermore we propose a set of features tailored for this task based on characteristics of the twitters. In particular, our approach relies on previous proposed features for sentiment analysis tasks.

## Usage

The folder has several scripts to test all the system or each component of the system:


