from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from query import *

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Restaurants</h1>"
                output += '<p><a href="/restaurants/new">Add new restaurant</a></p>'
                output += "<ul>List</ul>"

                restaurants = fetchRestaurants()

                for rest in restaurants:
                    output += "<li> %s </li>" % rest.name
                    output += "<p><a href='#'>Edit</a></p>"
                    output += "<p><a href='#'>Delete</a></p>"

                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                # output += "<h1>Enter new restaurant name</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Enter new restaurant name</h2><input name="newRestaurant" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return


            # edit name of rest
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Restaurants</h1>"
                output += '<p><a href="/restaurants/new">Add new restaurant</a></p>'
                output += "<ul>List</ul>"

                restaurants = fetchRestaurants()

                for rest in restaurants:
                    output += "<li> %s </li>" % rest.name
                    output += "<p><a href='#'>Edit</a></p>"
                    output += "<p><a href='#'>Delete</a></p>"

                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                print 'ok'
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                newRestaurantName = fields.get('newRestaurant')

                print "\n", " new rest: ", newRestaurantName
                addRestaurant(newRestaurantName[0])

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()


            # output = ""
            # output += "<html><body>"
            # output += " <h2> Okay, how about this: </h2>"
            # output += "<h1> %s </h1>" % messagecontent[0]
            # output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            # output += "</body></html>"
            # self.wfile.write(output)
            # print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
