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
                    output += "<p><a href='/%s/edit'>Edit</a></p>" % rest.id
                    output += "<p><a href='/%s/delete'>Delete</a></p>" % rest.id

                output += "</body></html>"
                self.wfile.write(output)
                return


            # Adding new restaurant
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Enter new restaurant name</h2><input name="newRestaurant" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return


            # Change name of the restaurant
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                #Get ID and Name of the restaurant
                restaurantId = self.path.split("/")[1]
                restaurant = fetchOneRest(restaurantId)

                output = ""
                output += "<html><body>"
                output += "<h3>%s</h3>" % restaurant.name
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><input name="changedRestaurantName" type="text" ><input type="submit" value="Submit"> </form>''' % restaurantId
                output += "</body></html>"
                self.wfile.write(output)
                return

            # Delete restaurant
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                #Get ID and Name of the restaurant
                restaurantId = self.path.split("/")[1]
                restaurant = fetchOneRest(restaurantId)

                output = ""
                output += "<html><body>"
                output += "<h1> Do you really want to delete %s ?</h1>" % restaurant.name
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><input type="submit" value="Submit"> </form>''' % restaurantId
                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                newRestaurantName = fields.get('newRestaurant')

                addRestaurant(newRestaurantName[0])

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    changedRestaurantName = fields.get('changedRestaurantName')
                restaurantId = self.path.split("/")[2]
                # print restaurantId, "rest id has"
                changeRestaurantName(restaurantId,changedRestaurantName[0])
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()


            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                # if ctype == 'multipart/form-data':
                #     fields = cgi.parse_multipart(self.rfile, pdict)
                restaurantId = self.path.split("/")[2]
                deleteRestaurant(restaurantId)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

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
