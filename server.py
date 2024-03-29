import sys;
import os;
from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse;
import Physics;
import random;

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        """
        GET Request function.
        """
        parsed = urlparse(self.path);
        if parsed.path in [ '/shoot.html' ]:
            fp = open('.'+self.path);
            content = fp.read();
            self.send_response( 200 );
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();
            self.wfile.write(bytes(content, "utf-8"));
            fp.close();
        elif parsed.path.startswith("/table-") and parsed.path.endswith(".svg"):
            try:
                with open('.'+self.path, 'rb') as fp:
                    content = fp.read();
                    self.send_response(200);
                    self.send_header("Content-type", "image/svg+xml");
                    self.send_header("Content-length", len(content));
                    self.end_headers();
                    self.wfile.write(content);
                    fp.close();
            except FileNotFoundError:
                self.send_response(404);
                self.end_headers();
                self.wfile.write(b"404: File not found");
        else:
            self.send_response(404);
            self.end_headers();
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"));

    def do_POST(self):
        """
        POST Request function.
        """
        parsed = urlparse(self.path);

        if parsed.path in [ '/setup.html' ]: #webpage to enter player and game names
            #read data
            post = self.rfile.read(int(self.headers['Content-length']));
            #parse data
            form = post.decode('utf-8').split('&');
            game = None;
            p1 = None;
            p2 = None;
            for value in form:
                name, data = value.split('=');
                if name == 'game':
                    game = data;
                elif name == 'p1':
                    p1 = data;
                elif name == 'p2':
                    p2 = data;
            #create database
            db = Physics.Database();
            db.createDB();
            self.poolGame = Physics.Game(gameName=game, player1Name=p1, player2Name=p2);
            #send 200 response back to browser
            response = "Game successfully created";
            self.send_response(200);
            self.send_header('Content-type', 'text/plain');
            self.end_headers();
            self.wfile.write(response.encode('utf-8'));

        elif parsed.path in [ '/play.html' ]: #webpage to start playing
            #create table
            table = Physics.Table();
        
            #place cue ball at starting position
            cueBallPos = Physics.Coordinate(Physics.TABLE_WIDTH/2.0,
                                            Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0);
            cueBall = Physics.StillBall(0, cueBallPos);
            table += cueBall;
        
            #place 15 coloured balls at starting positions, counting up and to the right
                #first row (bottom)
            pos1 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0+random.uniform(-3.0,3.0));
            ball1 = Physics.StillBall(1, pos1);
            table += ball1;
                #second row
            pos2 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0-Physics.BALL_RADIUS+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball2 = Physics.StillBall(2, pos2);
            table += ball2;
            pos3 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0+Physics.BALL_RADIUS+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball3 = Physics.StillBall(3, pos3);
            table += ball3;
                #third row
            pos4 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0-Physics.BALL_DIAMETER+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-2*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball4 = Physics.StillBall(4, pos4);
            table += ball4;
            pos5 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-2*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball5 = Physics.StillBall(5, pos5);
            table += ball5;
            pos6 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0+Physics.BALL_DIAMETER+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-2*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball6 = Physics.StillBall(6, pos6);
            table += ball6;
                #fourth row
            pos7 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0-3*Physics.BALL_RADIUS+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-3*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball7 = Physics.StillBall(7, pos7);
            table += ball7;
            pos8 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0-Physics.BALL_RADIUS+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-3*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball8 = Physics.StillBall(8, pos8);
            table += ball8;
            pos9 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0+Physics.BALL_RADIUS+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-3*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball9 = Physics.StillBall(9, pos9);
            table += ball9;
            pos10 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0+3*Physics.BALL_RADIUS+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-3*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball10 = Physics.StillBall(10, pos10);
            table += ball10;
                #fifth row (top)
            pos11 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0-2*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-4*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball11 = Physics.StillBall(11, pos11);
            table += ball11;
            pos12 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0-Physics.BALL_DIAMETER+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-4*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball12 = Physics.StillBall(12, pos12);
            table += ball12;
            pos13 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-4*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball13 = Physics.StillBall(13, pos13);
            table += ball13;
            pos14 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0+Physics.BALL_DIAMETER+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-4*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball14 = Physics.StillBall(14, pos14);
            table += ball14;
            pos15 = Physics.Coordinate(Physics.TABLE_WIDTH/2.0+2*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0),
                                      Physics.TABLE_WIDTH/2.0-4*Physics.BALL_DIAMETER+random.uniform(-3.0,3.0));
            ball15 = Physics.StillBall(15, pos15);
            table += ball15;

            svg = table.svg();
            html = f"""<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <title>Game</title>
                                <style>
                                    #container {{
                                        position: relative;
                                    }}
                                    #line {{
                                        position: absolute;
                                        top: 0;
                                        left: 0;
                                        pointer-events: none;
                                    }}
                                </style>
                            </head>
                            <body>
                                <div id="container">
                                    {svg}
                                </div>
                                <svg id="line" width="100%" height="100%">
                                    <line id="aiming-line" x1="0" y1="0" x2="0" y2="0" stroke="black" stroke-width="5"/>
                                </svg>
                                    <script>                       
                                        let isDragging = false;
                                        let initialX, initialY;
                                        const MAX_LINE_LENGTH = 500;

                                        function handleMouseDown(event) {{
                                            isDragging = true;
                                            initialX = event.clientX;
                                            initialY = event.clientY;

                                            const cueBall = document.querySelector('circle[fill="WHITE"]');
                                            const cueBallRect = cueBall.getBoundingClientRect();
                                            const cueX = cueBallRect.left + cueBallRect.width/2;
                                            const cueY = cueBallRect.top + cueBallRect.height/2;
                                            const aimingLine = document.getElementById('aiming-line');
                                            aimingLine.setAttribute('x1', cueX);
                                            aimingLine.setAttribute('y1', cueY);
                                            document.getElementById('line').style.display = 'block';
                                        }}

                                        function handleMouseMove(event) {{
                                            if (isDragging) {{
                                                const line = document.getElementById('aiming-line');

                                                const dx = event.clientX - initialX;
                                                const dy = event.clientY - initialY;
                                                const length = Math.sqrt(dx**2 + dy**2);
                                                if (length > MAX_LINE_LENGTH) {{
                                                    const ratio = MAX_LINE_LENGTH / length;
                                                    const newX = initialX + dx*ratio;
                                                    const newY = initialY + dy*ratio;
                                                    line.setAttribute('x2', newX);
                                                    line.setAttribute('y2', newY);
                                                }}
                                                else {{
                                                    line.setAttribute('x2', event.clientX);
                                                    line.setAttribute('y2', event.clientY);
                                                }}
                                            }}
                                        }}
                                        
                                        function handleMouseUp() {{
                                            if (isDragging) {{
                                                isDragging = false;
                                                document.getElementById('line').style.display = 'none';

                                                const dx = event.clientX - initialX;
                                                const dy = event.clientY - initialY;
                                                const velx = dx/MAX_LINE_LENGTH*10000;
                                                const vely = dy/MAX_LINE_LENGTH*10000;
                                                const speed = Math.sqrt(velx**2 + vely**2);
                                                const accx = 0;
                                                const accy = 0;
                                                if (speed > Physics.VEL_EPSILON) {{
                                                    accx = (-1)*(velx)/speed*Physics.DRAG;
                                                    accy = (-1)*(vely)/speed*Physics.DRAG;
                                                }}
                                            }}
                                        }}

                                        const balls = document.querySelectorAll('circle');
                                        balls.forEach(ball => {{
                                            if (ball.getAttribute('fill') === 'WHITE') {{ 
                                                ball.addEventListener('mousedown', handleMouseDown);
                                            }}
                                        }});

                                        document.addEventListener('mousemove', handleMouseMove);
                                        document.addEventListener('mouseup', handleMouseUp);
                                    </script>
                            </body>
                            </html>""";
            self.send_response(200);
            self.send_header('Content-type', 'text/html');
            self.send_header('Content-length', len(html));
            self.end_headers();
            self.wfile.write(html.encode('utf-8'));

        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );





if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();

