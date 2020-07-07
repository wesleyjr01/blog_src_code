# Coding a Blog from Scratch

The first post of this blog will cover on how to actually code a blog from scratch. This blog looks nothing like the fancy websites you see out there because **I used no theme**, **since one of the goals about this project is to learn as much as possible about web development**, I decided not to use a "ready to go theme", therefore the front end could be imensily improved using a freelancer theme like this one: https://startbootstrap.com/themes/freelancer.   


* ### Inspiration:
    * I have the habit of listening to PodCasts about Technology, Data Science and Geek Culture, and one of those that I like it a lot is called [Pizza de Dados](https://pizzadedados.com/), a PodCast about Data Science, Programming and Pizza, of course. And their hosts all have their own blogs, and the [blog from Leticia Portella](https://leportella.com/) is one that I often read. Her blog is a big inspiration for me to write my own, maybe because I see many similarities between our career paths, [transitioning from a not major programming career to a programming career](https://leportella.com/from-oceanographer-to-programmer.html) and [thoughts about development](https://leportella.com/dev-for-dummies.html). On another blog that really motivated me was the ["my experience with blogs"](https://leportella.com/dev-for-dummies.html), explained why she decided to write her own blog, and giving some technology tips, like using themes from [Jekyll Themes](http://jekyllthemes.org/), and host it with [GitHub Pages](https://pages.github.com/).   
<br>

* ### Writing a Web Server with Flask in Python:
    * Since my Web Development knowledge was nearly zero, I decided to take it to the hard way and build the blog from scratch to enhance my learning experience, but since I already had a reasonable Python Programming experience, I took a [Web Development Online Course using Flask as a Web Server Framework, and Python](https://www.udemy.com/course/the-complete-python-web-course-learn-by-building-8-apps/). The [Flask](https://flask.palletsprojects.com/en/1.1.x/) documentation is also very extensive, which helps a lot.   
<br>

* ### Writing HTML Templates, Basic CSS and JavaScript.
    * Even though the application developed at the Web Course I was taking was not a blog, things like building a Header, customizing some basic elements like Forms and Buttons with HTML Templates and CSS were really useful, so I kinda learned the very basics of HTML, CSS and JavaScript from there, and it was enough to build a very simple application like a Blog with those resources. Some JavaScript interactions given by the [Bootstrap4](https://getbootstrap.com/) elements helped a lot too.   
<br>

* ### Managing  Users and Posts with MongoDB and Pymongo.
    * Even though the data of a very simple application like this one can be handled be files like .csv files, I really wanted to program my own Database and handle the users registers and posts, and design the connection between them. Since I already had some familiarity with SQL Databases, I gave it a try to a Non-SQL database this time, using [MongoDB](https://www.mongodb.com/). The installation and configuration of MongoDB is actually very simple, you can find pretty much everything you need to know and configure on the official website, much simpler than configure an SQL Engine like [SQLAlchemy](https://www.sqlalchemy.org/), even though SQLALchemy is very powerful, and allows you to write the relation of the data inside the definition of the models of the project, which is a great architecture in my opinion.   
<br>

* ### Serving the Application in a Linux Server with Digital Ocean:
    * As I mentioned, it wouldn't be a *"from scratch"* kind of thing if I had used an easier hosting service like [Github Pages](https://pages.github.com/), or even on [Heroku](https://www.heroku.com/), which would definitely be ok for this simple task, but I wanted to actually serve it on my on machine, so I bought a very small machine on [Digital Ocean](https://www.digitalocean.com/) to host my application, and I had to learn how to configure it in the first place (Oh boy, that was a lot of work). Thankfully, there is a very detailed tutorial on the Digital Ocean's community to make things easier, called [How To Serve Flask Applications With uWSGI and Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04), but I had never configured Nginx and uWSGI before, so at least for me it took a lot of hours to get things done. But it worked! 
![Benjamin Bannekat](https://cdn0.tnwcdn.com/wp-content/blogs.dir/1/files/2020/01/q3V3Xe3-796x531.jpg)  
<br>
    
* ### Blog Source Code on GitHub:
    * I plan to make a footer and a pagination on the near future, but that was a suitable starting point already, [here is the source code if you want to look or clone it](https://github.com/wesleyjr01/blog_src_code). Something else that I might do, if possible, is use some kind of auto-translation, so the post’s content would be available both in English and Portuguese.