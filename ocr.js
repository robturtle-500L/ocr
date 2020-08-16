/**
 * creates a 20x20 pixel canvas, with 10x of scale.
 */
(function (global) {
  'use strict';

  var CANVAS_WIDTH = 200;
  var TRANSLATED_WIDTH = 20;
  var PIXEL_WIDTH = 10;

  var EMPTY_COLOR = '#000000';
  var FILLED_COLOR = '#0000ff';

  var data;
  var canvas = document.getElementById('canvas');
  var ctx = canvas.getContext('2d');

  function onload() {
    resetCanvas();
  }

  function resetCanvas() {
    data = new Array(400).fill(0);
    ctx.fillStyle = EMPTY_COLOR;
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_WIDTH);
    drawGrid(ctx);
  }

  function drawGrid(ctx) {
    for (var i = PIXEL_WIDTH; i < CANVAS_WIDTH; i += PIXEL_WIDTH) {
      ctx.strokeStyle = FILLED_COLOR;
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i, CANVAS_WIDTH);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(0, i);
      ctx.lineTo(CANVAS_WIDTH, i);
      ctx.stroke();
    }
  }

  function onMouseMove(e) {
    if (!canvas.isDrawing) {
      return;
    }
    fillSquare(e.clientX, e.clientY);
  }

  function onMouseDown(e) {
    canvas.isDrawing = true;
    fillSquare(e.clientX, e.clientY);
  }

  function onMouseUp(_e) {
    canvas.isDrawing = false;
  }

  function fillSquare(clientX, clientY) {
    var x = Math.floor((clientX - canvas.offsetLeft) / PIXEL_WIDTH);
    var y = Math.floor((clientY - canvas.offsetTop) / PIXEL_WIDTH);
    data[(x - 1) * TRANSLATED_WIDTH + y - 1] = 1;
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(x * PIXEL_WIDTH, y * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH);
  }

  /*
   * @param type: 'train' | 'test'
   */
  function addSample(type) {
    var digitVal = document.getElementById('digit').value;
    if (!digitVal || data.indexOf(1) < 0) {
      return alert(
        'Please type and draw a digit value in order to train the network',
      );
    }
    var digit = parseInt(digitVal);
    if (isNaN(digit)) {
      return alert('invalid digit: ' + digitVal);
    }
    sendData({ y0: data, label: digit, type: type });
  }

  function sendData(json) {
    var xmlhttp = new XMLHttpRequest();
    var payload = JSON.stringify(json);
    xmlhttp.open('POST', 'http://localhost:5000');
    xmlhttp.setRequestHeader('Content-Type', 'application/json');
    xmlhttp.onload = sendDataEnd;
    xmlhttp.onerror = sendDataError;
    xmlhttp.send(payload);
    return xmlhttp;
  }

  function sendDataEnd(e) {
    var xmlHttp = e.target;
    if (xmlHttp.status !== 200) {
      return alert('Server returned status ' + xmlHttp.status);
    }
    var res = JSON.parse(xmlHttp.responseText);
    console.log(res);
    if (res.type === 'test') {
      alert('The neural network says it is a ' + res.result);
    }
  }

  function sendDataError(e) {
    alert('Error connecting to server: ' + e.target.statusText);
  }

  canvas.onmousemove = onMouseMove;
  canvas.onmousedown = onMouseDown;
  canvas.onmouseup = onMouseUp;

  global.ocrDemo = {
    onload: onload,
    resetCanvas: resetCanvas,
    train: addSample.bind(null, 'train'),
    test: addSample.bind(null, 'test'),
  };
})(window);
