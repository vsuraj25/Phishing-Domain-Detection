[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

<div id="top"></div>

<div align="center">
  <a href="https://github.com/vsuraj25">
    <img src="https://img.icons8.com/clouds/100/domain.png" alt="Logo" width="80" height="80"/> 
  </a>

    
<h3 align="center">Phishing URL Detection</h3>

 <p align="center">
    Machine Learning (Internship)
    <br />
    <a href="https://github.com/vsuraj25"><strong>Explore my Repositories. »</strong></a>
    <br />
    <br />
    <a href="#intro">Introduction</a>
    ·
    <a href="#data"> Data Information</a>
    ·
    <a href="#contact">Contact</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## **Problem Statement**
* With the development of Internet technology, network security is under diverse threats. In
particular, attackers can spread malicious uniform resource locators (URL) to carry out
attacks such as phishing and spam. The research on malicious URL detection is
significant for defending against these attacks. However, there are still some problems.
For instance, malicious features cannot be extracted efficiently. Some existing detection
methods are easy to evade by attackers. We design a machine learning model, to detect whether the url can be risky or not.



## **Deployed app**
[![App Screenshot](https://user-images.githubusercontent.com/55409076/241212064-3fc50090-720a-4696-b267-6684936899ea.png)](https://phishing-domain-detector.onrender.com/)

[Deployed app link](https://phishing-domain-detector.onrender.com/)

<!-- GETTING STARTED -->
<div id="intro"></div>

## **Introduction**
*  This project aims to develop a machine learning model that can detect risky urls by digging deep into the url features. The goal is to develop a model that can learn the features of URL and return a accurate results for the legitimacy of the url. We have tried to generate the features in an exactly similar way as to the research. 
All the models and data are tracked and maintained using DVC and MLflow.
  
 
<div id="data"></div>
<!-- USAGE EXAMPLES -->

## **Dataset Information**

* Download the original dataset here : 
  [Phishing Web Site Dataset](https://archive.ics.uci.edu/ml/datasets/phishing+websites)

 
* This Dataset was part of the reasearch for Phishing Domain Detection by Rami M. Mohammad, Fadi Thabtah and Lee McCluskey.
* The Dataset was published in 2014. 
* The Dataset contains 11055 records and 31 features. 
* The dataset is split into two subsets: a training set and a test set. 

* **Attribute Information**

1. `IP Address Usage`: Detects the presence of an IP address in the URL instead of a domain name.
2. `Long URL to Hide Suspicious Part`: Identifies long URLs that may be used to hide suspicious parts or obfuscate the actual destination.
3. `URL Shortening Services` (e.g., TinyURL): Detects the use of URL shortening services, which can be used to mask the actual destination URL.
4. `URL's with "@" Symbol`: Checks for the presence of an "@" symbol in the URL, which is uncommon and potentially indicative of a phishing attempt.
5. `Redirecting using "//"`: Identifies the use of double slashes ("//") in the URL, which can be used for URL redirecting and potentially lead to malicious websites.
6. `Adding Prefix or Suffix to Domain`: Detects the addition of prefixes or suffixes to a legitimate domain name, which can be an attempt to deceive users.
7. `Subdomain and Multi Subdomains`: Checks for the presence of subdomains or multiple subdomains in the URL, which can be used for phishing or impersonation.
8. `HTTPS (Hyper Text Transfer Protocol with Secure Sockets Layer)`: Determines if the website uses HTTPS, a secure protocol that encrypts data transmission between the user and the website.
9. `Domain Registration Length`: Examines the length of time the domain has been registered, as longer registrations can indicate a more trustworthy website.
10. `Favicon`: Verifies the presence of a favicon, the small icon displayed in the browser tab, which is often absent in fake or phishing websites.
11. `Using Non-Standard Port`: Detects the use of non-standard ports in the URL, which can be used for phishing attacks.
12. `Existence of "HTTPS" Token in the Domain`: Checks if the domain contains the term "HTTPS," which can be a sign of a fake website attempting to deceive users.
13. `Request URL`: Analyzes the URL to determine if it matches the expected URL of the website.
14. `URL of Anchor`: Checks the URL linked to an anchor tag (<a>) to ensure it corresponds to the expected destination.
15. `Links in <Meta>, <Script>, and <Link> tags`: Examines the URLs present in these HTML tags to identify any discrepancies or potentially malicious links.
16. `Server Form Handler (SFH)`: Verifies if the form's action attribute points to a different domain, which can indicate a phishing attempt.
17. `Submitting Information to Email`: Detects if the form's action attribute submits data to an email address, which can be indicative of a phishing attack.
18. `Abnormal URL`: Checks for any unusual or suspicious patterns in the URL that could indicate phishing or impersonation attempts.
19. `Website Forwarding`: Identifies the use of JavaScript or HTML redirects, which can redirect users to malicious websites.
20. `Status Bar Customization`: Checks if the website attempts to customize or hide the browser's status bar, which can be a sign of malicious intent.
21. `Disabling Right Click`: Detects if the website disables the right-click function, which can be used to prevent users from accessing browser functionalities and potentially hide malicious actions.
22. `Using Pop-up Window`: Identifies the use of pop-up windows, which can be used for phishing or to deceive users.
23. `IFrame Redirection`: Checks for the presence of hidden iframes, which can redirect users to malicious websites or content.
24. `Age of Domain`: Determines the length of time the domain has been active, as newer domains are more likely to be associated with malicious activities.
25. `DNS Record`: Checks the DNS record for inconsistencies or signs of tampering that can indicate a malicious website.
26. `Website Traffic`: Examines the website's traffic and popularity as an indicator of legitimacy or suspicious activity.
27. `PageRank`: Assesses the website's PageRank, a metric that indicates its reputation and relevance, to determine its trustworthiness.
28. `Google Index`: Determines if a website is indexed by Google. Phishing webpages often aren't indexed due to their short lifespan.
29. `Number of Links Pointing to Page`: Evaluates the legitimacy of a webpage based on the number of external links. Phishing sites typically lack external links, while legitimate sites have at least 2.
30. `Statistical-Reports Based Feature`: Relies on statistical reports from organizations like PhishTank and StopBadware. These reports identify top phishing domains, IPs, and provide valuable insights.
31. `Result`: Whether the website is phishing or not.

- For detailed information about the features, checkout - https://archive.ics.uci.edu/ml/machine-learning-databases/00327/Phishing%20Websites%20Features.docx

<p align="right">(<a href="#top">back to top</a>)</p> 

<!-- USAGE EXAMPLES -->
## **Project Architecture**

[![Project Architecture - 1](https://user-images.githubusercontent.com/55409076/238178973-1895aaba-78a1-48eb-be30-3f777d82ad06.png)](https://github.com/vsuraj25)
[![Project Architecture - 2](https://user-images.githubusercontent.com/55409076/241217998-09d85c63-2ac8-40de-9d0e-58dff38691a9.png)](https://github.com/vsuraj25)

## **Latency for model response**
 
* 7.8 Seconds

## **Project Demo Youtube Video**
[![Project Youtube Video]()]()

## **Linkedin Post**
[![Phishing URL Detection](https://img.shields.io/badge/Phishing_URL_Detection_Project-eeeeee?style=for-the-badge&logo=linkedin&logoColor=ffffff&labelColor=0A66C2)]()


## **About this Internship Project**

* Project Title : Phishing URL Detection
* Technologies : Machine Learning
* Domain : Cyber Security
* Project Difficulties level : Intermediate / Advance

## **Requirements**
* Python 3.8
* Numpy
* Pandas
* BeautifulSoup4
* Flask
* Pytest
* Tox
* DVC
* MLFlow
* Checkout requirements.txt for more information.

## **Technologies used**
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)
![DVC](https://img.shields.io/badge/DVC-945DD6?style=for-the-badge&logo=dataversioncontrol&logoColor=white)
![MLFlow](https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=for-the-badge&logo=numpy&logoColor=blue)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)


## **Tools used**
![Visual Studio Code](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Render](https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white)
![MLFlow](https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=for-the-badge&logo=numpy&logoColor=blue)

<!-- CONTACT -->
<div id="contact"></div>

## **Contact**
[![Suraj Verma | LinkedIn](https://img.shields.io/badge/Suraj_Verma-eeeeee?style=for-the-badge&logo=linkedin&logoColor=ffffff&labelColor=0A66C2)][reach_linkedin]
[![Suraj Verma | G Mail](https://img.shields.io/badge/sv255255-eeeeee?style=for-the-badge&logo=gmail&logoColor=ffffff&labelColor=EA4335)][reach_gmail]
[![Suraj Verma | Portfolio](https://img.shields.io/badge/My_Portfolio-eeeeee?style=for-the-badge)][reach_portfolio]

[reach_linkedin]: https://www.linkedin.com/in/suraj-verma-982b31157/
[reach_gmail]: mailto:sv255255@gmail.com?subject=Github
[reach_portfolio]: https://vsuraj25.github.io/


<p align="right">(<a href="#top">back to top</a>)</p>



