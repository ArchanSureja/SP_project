 //  intii zation of digram div
 var namespace = joint.shapes;

 var graph = new joint.dia.Graph({}, { cellNamespace: namespace });
 
 var paper = new joint.dia.Paper({
     el: document.getElementById('diagram-canvas'),
     model: graph,
     // width: 600,
     // height: 100,
     gridSize: 1,
     
     cellViewNamespace: namespace
   });
 var content = document.getElementById('content').value;
 console.log(content);
 if(content!="")
{
    content  = content.replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
    console.log(content);
    let JsonOfGraph = JSON.parse(content);
    graph.fromJSON(JsonOfGraph);
}
//  onclick adding shapes to the digram
 function addRectTOdiagram()
 {
     var rect = new joint.shapes.standard.Rectangle();
         rect.position(100, 30);
         rect.resize(100, 40);
         rect.attr({
             body: {
                 fill: 'lightblue'
             },
             label: {
                 text: 'Text',
                 fill: 'black'
             }
         });
         rect.addTo(graph);
 }
 function addCircleTOdiagram()
 {
    var circle = new joint.shapes.standard.Circle();
    circle.position(100, 30);
    circle.resize(100, 100);
    circle.attr({
        body: {
            fill: 'lightblue'
        },
        label: {
            text: 'Text',
            fill: 'black'
        }
    });
    circle.addTo(graph);
 }
 function addDiamondTOdiagram()
 {
    var polygon = new joint.shapes.standard.Polygon();
    polygon.resize(100, 100);
    polygon.position(250, 210);
    polygon.attr('label/text', 'text');
    polygon.attr('body/refPoints', '0,10 10,0 20,10 10,20');
    polygon.addTo(graph)
 }
 function addEllipseTOdiagram()
 {
    var ellipse = new joint.shapes.standard.Ellipse();
    ellipse.resize(150, 100);
    ellipse.position(425, 10);
    ellipse.attr('root/title', 'joint.shapes.standard.Ellipse');
    ellipse.attr('label/text', 'Text');
    ellipse.attr('body/fill', 'lightblue');
    ellipse.addTo(graph);
 }
 function addLinkTOdiagram()
 {
    
    var link = new joint.shapes.standard.Link();
     link.prop('source', { x: 20, y: 20 });
     link.prop('target', { x: 100, y: 20 });
     link.attr('root/title', 'joint.shapes.standard.Link');
     link.attr('line/stroke', 'black');
     link.addTo(graph);
 }
 function addDlinkTOdiagram()
 {
    var doubleLink = new joint.shapes.standard.DoubleLink();
doubleLink.prop('source', { x: 20, y: 20});
doubleLink.prop('target', { x: 100, y: 20 });
doubleLink.attr('root/title', 'joint.shapes.standard.DoubleLink');
doubleLink.attr('line/stroke', '#30d0c6');
doubleLink.addTo(graph);
 }

// deleting of the selected element 
var selectedCell;
var degree = 0;
var pre_selectedCell;
paper.on('cell:pointerclick', (cellView) => {
    console.log("clicked")
    pre_selectedCell = selectedCell;
    selectedCell = cellView.model;
    color=selectedCell.attributes.attrs.body.fill
    // Perform actions with the selected cell
    if(pre_selectedCell!=undefined)
    {
        pre_selectedCell.attr('body/fill',color)
    }
    selectedCell.attr('body/fill','red');
    console.log(pre_selectedCell);
    console.log('Selected Cell ID:', selectedCell.id);
    console.log('Selected Cell Type:', selectedCell.get('type'));
    console.log('Selected Cell Position:', selectedCell.position());
  
    
  
});
// Function to rotate a point (x, y) around the origin (0, 0) by a given angle in degrees
function rotatePoint(x, y, angleDegrees) {
    const angleRadians = (angleDegrees * Math.PI) / 180;
    const newX = x * Math.cos(angleRadians) - y * Math.sin(angleRadians);
    const newY = x * Math.sin(angleRadians) + y * Math.cos(angleRadians);
    return { x: newX, y: newY };
}

// Function to rotate a link by changing its target coordinates
function rotateLink(link, angleDegrees) {
    const source = link.source();
    const target = link.target();

    // Calculate the new target coordinates based on the rotation angle
    const rotatedTarget = rotatePoint(target.x - source.x, target.y - source.y, angleDegrees);

    // Set the new target coordinates for the link
    link.target({ x: source.x + rotatedTarget.x, y: source.y + rotatedTarget.y });
}

function rotate()
{
    if(selectedCell!=undefined)
    {
       if(!(selectedCell instanceof joint.shapes.standard.DoubleLink) && !(selectedCell instanceof joint.shapes.standard.Link))
       {
        console.log("rotate")
        degree += 5;
        selectedCell.rotate(degree,origin);
        selectedCell.rotate(degree)
       }
       else
       {
            console.log("rotating the link")
            rotateLink(selectedCell, 5);
       }

    }
}
function change_color()
{
    if(selectedCell!=undefined)
    {
        let c = prompt("enter new color");
        selectedCell.attr('body/fill', c);
    }
}
function change_text()
{
    if(selectedCell!=undefined)
    {
        if(!(selectedCell instanceof joint.shapes.standard.DoubleLink) && !(selectedCell instanceof joint.shapes.standard.Link))
        {
        console.log("changing text of element")
        let text = prompt("enter text here");
        selectedCell.attr('label/text',text)
        }
        
    }
}
function delete_element()
{
        
        graph.removeCells(selectedCell);
        console.log('removed element');
    
}
function set_content()
{
    let graph_json=graph.toJSON();
    console.log(graph_json);
    let string_ = JSON.stringify(graph_json);
    console.log(string_);
    document.getElementById('content').value = string_;
    console.log(document.getElementById('content').value); 
    console.log("above printed content is set to the hidden field");
    window.alert("your changes are saved");
}

function downloadDiagram(diagram_id)
{
   divContainer_id = "diagram-container-"+diagram_id;
   var outerDiv = document.getElementById(divContainer_id);
   var svgElement = outerDiv.querySelector('svg');
   console.log(svgElement.id);
   var svgData = new XMLSerializer().serializeToString(svgElement);
   var svgWidth = svgElement.clientWidth; // Get the client width of the SVG element
   var svgHeight = svgElement.clientHeight;
   var img = new Image();
   console.log(svgData)
    img.onload = function() {
        var canvas = document.createElement('canvas');

        
        canvas.width =  svgWidth;
        canvas.height = svgHeight;
        var ctx = canvas.getContext('2d');
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);

        var jpegData = canvas.toDataURL('image/jpeg');

        // Trigger download
        var link = document.createElement('a');
        link.download = 'diagram_to_jpeg.jpg';
        link.href = jpegData;
        link.click();
    };
    img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
}
