
class Display {

     constructor(document, canvasWidth, canvasHeight, world, worldWidth, worldHeight) {
          this.world = world;
          this.worldWidth = worldWidth;
          this.worldHeight = worldHeight;

          this.setCanvasProperties(document, canvasWidth, canvasHeight);
     }

     setCanvasProperties(document, width, height) {
          var canvasElement = document.getElementById('canvas');
          this.canvas = canvasElement.getContext('2d');
          this.canvasWidth = canvasElement.width = width;
          this.canvasHeight = canvasElement.height = height;
     }

     displayStats(farthestDistTraveled, elapsedTime, totalDistTraveled) {
          this.canvas.font = '20pt Calibri';
          this.canvas.fillStyle = 'black';

          this.canvas.fillText('Best Distance: ' + round(farthestDistTraveled) + ' m', 100, 50);
          this.canvas.fillText('Time Elapsed: ' + Math.round(elapsedTime*10)/10 + ' s', 100, 100);
          this.canvas.fillText('Total Distance: ' + round(totalDistTraveled) + ' m', 100, 200);
          // canvas.fillText('Keystate: ' + keyPressed,100,150)
          // action_strings[keyState] = keyPressed
     }

     draw(node) {

         var pos = node.GetPosition();
         var fList = node.GetFixtureList();
         if (fList !== null) {

             var shape = fList.GetShape();
             var shapeType = shape.GetType();

             if (shapeType == b2Shape.e_circleShape) {
                 this.canvas.beginPath();
                 this.canvas.arc(this.xToCanvas(pos.x), this.yToCanvas(pos.y), (40.0 / 1054.0) * this.canvasWidth, 0, 2 * PI, false);
                 this.canvas.fillStyle = '#FFF3C3';
                 this.canvas.fill();
                 this.canvas.lineWidth = 5;
                 this.canvas.strokeStyle = '#003300';
                 this.canvas.stroke();
             } else {
                 this.canvas.beginPath();

                 var vtx = shape.m_vertices;
                 var r = node.GetAngle();
                 var sinr = sin(r), cosr = cos(r);
                 var x0 = (vtx[0].x*cosr-vtx[0].y*sinr), y0 = (vtx[0].x*sinr+vtx[0].y*cosr);

                 this.canvas.moveTo(this.xToCanvas(pos.x + x0), this.yToCanvas(pos.y+ y0));

                 for (var i = 1; i < vtx.length; i++) {
                     this.canvas.lineTo(this.xToCanvas(pos.x+(vtx[i].x*cosr-vtx[i].y*sinr)),
                         this.yToCanvas(pos.y+(vtx[i].x*sinr+vtx[i].y*cosr)));
                 }
                 this.canvas.lineTo(this.xToCanvas(pos.x + x0), this.yToCanvas(pos.y + y0));

                 this.canvas.fillStyle = '#FFF3C3';
                 this.canvas.fill();
                 this.canvas.lineWidth = 5;
                 this.canvas.strokeStyle = '#003300';
                 this.canvas.stroke();
             }
         }
     }

     /* Clear the current frame. */
     clearCurrentFrame() {
          this.canvas.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
     }

     /* Draws all of the nodes in the world */
     drawWorld() {
          var node = this.world.world.GetBodyList();

          while (node.GetNext() !== null) {
               this.draw(node);
               node = node.GetNext()
          }
     }

     xToWorld(x) {
         return this.worldWidth * x / this.canvasWidth
     }

     yToWorld(y) {
         return this.worldHeight * (this.canvasHeight - y) / this.canvasHeight
     }

     xToCanvas(x) {
         // The x coordinate starts at 0 and ends at 500
         return this.canvasWidth * x / this.worldWidth
     }

     yToCanvas(y) {
         // The y coordinate starts at 500 and ends at 0
         return this.canvasHeight * (this.worldHeight - y) / this.worldHeight
     }

     toCanvas(x, y) {
         return [this.xToCanvas(x), this.yToCanvas(y)]
     }

}






