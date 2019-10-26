import logging
import json

import azure.functions as func


def main(req: func.HttpRequest) -> str:
    logging.info('Get LinkedIn Data function has been called')

    return """[
	{
		"general": {
			"imgUrl": "https://media.licdn.com/dms/image/C4D03AQHvsHMqAT2WyQ/profile-displayphoto-shrink_100_100/0?e=1577318400&v=beta&t=sihcxUYzZ199Rajt6FxCcSE7f4A9n0yrQKnFpyWi0dE",
			"fullName": "Tomas Ye",
			"headline": "Software Engineer at Amazon",
			"company": "Amazon",
			"location": "Luxembourg",
			"connections": "500+ connections",
			"profileUrl": "https://www.linkedin.com/in/tomas-ye/",
			"connectionDegree": "2nd",
			"vmid": "ACoAACKa1l0BcfqbQ5CtSLL0hRllVlUGHywDCKU",
			"linkedinSalesNavigatorUrl": "https://www.linkedin.com/sales/people/ACoAACKa1l0BcfqbQ5CtSLL0hRllVlUGHywDCKU,name",
			"description": "Ready and willing to solve problems with technology.In today's world, we have abundant amounts of data. However, extracting the relevant information from this data, visualising it, interpreting it and, most importantly, making good decisions based on it, is not always as straightforward as one would hope. This is where people like me come into play.I am a junior software developer, with strong background in mathematics, trying my best at tackling technological challenges the world has to offer. Whether you need a fancy web application or a machine learning model, I can do it!Technically, I am proficient with Java, JavaScript and Python, I can juggle databases with SQL and I have experience with creating machine learning models via TensorFlow and SciKitLearn.Mentally, I am obsessed with innovation and self-improvement, always looking for ways to challenge myself and expand my limits.My free time I devote to practicing gymnastics, reading and working on my blog.Is there a problem I can help you with? Ping me!",
			"subscribers": "765",
			"connectionsUrl": "https://www.linkedin.com/search/results/people/?facetNetwork=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH",
			"firstName": "Tomas",
			"lastName": "Ye"
		},
		"jobs": [
			{
				"companyName": "Amazon",
				"companyUrl": "https://www.linkedin.com/company/amazon/",
				"jobTitle": "Software Engineer",
				"dateRange": "Jul 2019 – Present",
				"location": "Luxembourg",
				"description": "Making Amazon great with technology!\n\nDeveloped an end-to-end data visualisation solution which provides valuable insight into Amazon Transportation network. The tool is used by business operators to schedule transportation vehicles with increased precision related to the forecasted demand. The increased precision of scheduling directly translates into monetary savings for the company as ordered vehicles are utilised more efficiently.\n\nI had several key responsibilities in the project:\n\n1) Designed the project and laid down the necessary computational infrastructure in the AWS cloud (Continuous Deployment Pipeline, Automatised unit and integration tests ...)\n\n2) Developed a \"Proof Of Concept\" version of the project, pitched it to the rest of my team and, ultimately, convinced them that the project is meaningful. The technological stack of the project included a MySQL database, Google Guice powered Java Backend server application and an Angular 6 web browser client. \n\n3) Managed the onboarding of new interns into the project and mentored them throughout the later stages of the project development. \n\n4) Finally, completely handed off the project to the interns. It brought me great pleasure to see the product flourish, despite me not being involved in the development anymore."
			},
			{
				"companyName": "Amazon",
				"companyUrl": "https://www.linkedin.com/company/amazon/",
				"jobTitle": "Software Engineer Intern",
				"dateRange": "Mar 2019 – Jun 2019",
				"location": "Luxembourg",
				"description": "Improving Amazon’s transportation network with software technologies. \n\nMy main project is a web-based application for configuring and scheduling SQL jobs, outputs of which are used by many other Amazon teams for operational decision making. Before the app, these jobs had to be configured and scheduled manually through Excel, hence a lot of wasted human effort.\n\nThe app is already saving hours of manual labor every week and provides additional visibility to the Amazon transportation network. \n\nTechnologies utilised in the project: Java, SQL, Angular 6, AWS"
			},
			{
				"companyName": "SAP Concur",
				"companyUrl": "https://www.linkedin.com/company/sapconcur/",
				"jobTitle": "Software Engineer Intern",
				"dateRange": "Jul 2018 – Jan 2019",
				"location": "Prague, The Capital, Czech Republic",
				"description": "Development of SAP’s internal applications for market and business departments. \n\nRecognized as among the best technical interns of SAP's Summer 2018 internship program, my day to day duties were: \n\n1) Extending existing Java APIs for handling and monitoring communication between SAP’s major databases \n\n2) Adding new features for user interface of team’s Angular web apps to enhance usability and experience \n\n3) Improving build and deployment pipelines according to the DevOps philosophy, which increased the team’s efficiency in its delivery."
			},
			{
				"companyName": "Sator IT",
				"companyUrl": "https://www.linkedin.com/search/results/index/?keywords=Sator%20IT",
				"jobTitle": "Dotnet Developer",
				"dateRange": "Aug 2016 – May 2017",
				"location": "Prague, The Capital, Czech Republic",
				"description": "Given the responsibility to take over a running C# .Net web reservation system, the main responsibilities were: \n\n1) Extending the server API to satisfy ever increasing customer requirements as the business was growing\n \n2) Utilizing JavaScript for enhancing the client facing UI to provide the best possible user experience."
			}
		],
		"schools": [
			{
				"schoolUrl": "https://www.linkedin.com/school/11709/?legacySchoolId=11709",
				"schoolName": "Charles University in Prague",
				"degree": "Master's degree",
				"degreeSpec": "Pure Mathematics",
				"dateRange": "2018 – 2019",
				"description": ""
			},
			{},
			{
				"schoolUrl": "https://www.linkedin.com/school/11709/?legacySchoolId=11709",
				"schoolName": "Charles University in Prague",
				"degree": "Bachelor's degree",
				"degreeSpec": "Mathematics and Computer Science",
				"dateRange": "2015 – 2018",
				"description": ""
			},
			{}
		],
		"details": {
			"linkedinProfile": "https://www.linkedin.com/in/tomas-ye",
			"twitter": "thetumblingtom",
			"birthday": "January 29",
			"mail": "tommygamba17@gmail.com"
		},
		"skills": [
			{
				"name": "Mathematics",
				"endorsements": "9"
			},
			{
				"name": "Programming",
				"endorsements": "8"
			},
			{
				"name": "Public Speaking",
				"endorsements": "5"
			},
			{
				"name": "Statistics",
				"endorsements": "2"
			},
			{
				"name": "Machine Learning",
				"endorsements": "0"
			},
			{
				"name": "Object-Oriented Programming (OOP)",
				"endorsements": "4"
			},
			{
				"name": "Software Development",
				"endorsements": "2"
			},
			{
				"name": "Python",
				"endorsements": "4"
			},
			{
				"name": "Java",
				"endorsements": "5"
			},
			{
				"name": "C#",
				"endorsements": "2"
			},
			{
				"name": "ASP.NET",
				"endorsements": "0"
			},
			{
				"name": ".NET MVC",
				"endorsements": "0"
			},
			{
				"name": "HTML",
				"endorsements": "0"
			},
			{
				"name": "JavaScript",
				"endorsements": "2"
			},
			{
				"name": "CSS",
				"endorsements": "0"
			},
			{
				"name": "SQL",
				"endorsements": "3"
			},
			{
				"name": "Microsoft Word",
				"endorsements": "0"
			},
			{
				"name": "Microsoft Excel",
				"endorsements": "0"
			},
			{
				"name": "Microsoft PowerPoint",
				"endorsements": "0"
			},
			{
				"name": "Microsoft Office",
				"endorsements": "0"
			},
			{
				"name": "Python (Programming Language)",
				"endorsements": "1"
			},
			{
				"name": "Teaching",
				"endorsements": "3"
			},
			{
				"name": "Sports Coaching",
				"endorsements": "1"
			},
			{
				"name": "Leadership",
				"endorsements": "1"
			},
			{
				"name": "Linear Algebra",
				"endorsements": "1"
			}
		],
		"allSkills": "Mathematics, Programming, Public Speaking, Statistics, Machine Learning, Object-Oriented Programming (OOP), Software Development, Python, Java, C#, ASP.NET, .NET MVC, HTML, JavaScript, CSS, SQL, Microsoft Word, Microsoft Excel, Microsoft PowerPoint, Microsoft Office, Python (Programming Language), Teaching, Sports Coaching, Leadership, Linear Algebra",
		"query": "https://www.linkedin.com/in/tomas-ye/"
	}
]"""






