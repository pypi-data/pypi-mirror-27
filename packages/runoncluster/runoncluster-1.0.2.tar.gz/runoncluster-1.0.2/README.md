runoncluster
===

Submits jobs to the tl-app

Installation
---

	pip install runoncluster

Usage
---

	runoncluster script.Rmd inputs.json config.json

Configuration
---

**RMarkdown Script***

Use the `params` feature for passing inputs to the script:

	---
	title: "Sample Script"
	output: 
	  html_document:
	    self_contained: false
	params:
	  sample_size: 10000
	---

	### Session Information

	```{r sessionInfo, echo=FALSE, results="asis"}
	sessionInfo()
	```

**inputs.json**

Set the values of parameters as key/value pairs in a json file:

	{
		"sample_size": 10000
	}

**config.json**

The configuration file lets the CLI know where to send the job. Here is an example:

	{
		"base_url": "https://tl-app-rvit.herokuapp.com/",
		"ghap_username": "${GHAP_USERNAME}",
		"ghap_password": "${GHAP_PASSWORD}",
		"ghap_ip": "${GHAP_IP}",
		"token": "admintoken"
	}

The special `${VAR_NAME}` syntax will read the value from an environment variable before pushing it to the server.

Right now, you have to ask a developer for an API token. Improved UX coming soon!





