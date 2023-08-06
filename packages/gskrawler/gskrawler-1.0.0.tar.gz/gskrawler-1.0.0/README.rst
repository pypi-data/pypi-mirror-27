gskrawler
==============

gskcrawler will enter your domain and scan every page of your website, extracting page titles, descriptions, keywords, and links etc..
----


Description: gskrawler
        ==============
                
        gskcrawler will enter your domain and scan every page of your website, extracting page titles, descriptions, keywords, and links etc..

        Requirements
        ============================
        BeautifulSoup4
        requests
        urllib3 1.22
        

        Commands
        ============================
        <head>
        ------------

				gskrawler.head(url)

		<title> 
		------------

				gskrawler.title(url)

		<body>
		------------

				gskrawler.body(url)

		response in html format
		------------

				gskrawler.html(url)

		links in a website
		------------

				gskrawler.links(url)

		class elements
		------------

				gskrawler.tagclass(url,tagname,classname)

		id elements
		------------

				gskrawler.tagid(url,tagname,idname)

		emails in a website
		------------

				gskrawler.emails(url)

		images in a website
		------------

				gskrawler.images(url)


        ----
        
        Example Code
        ------------
        
        Open Python Interpreter::
        
            >>> import gskrawler
            >>> gskrawler.emails('https://www.fisglobal.com/')
            >>> gskrawler.images('https://www.fisglobal.com/')
            >>> gskrawler.head('https://www.fisglobal.com/')
            >>> gskrawler.tagclass('https://www.naukri.com/','ul','set')
