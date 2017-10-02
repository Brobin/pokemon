Chart.Controller.prototype.getElementsAtEvent = function(e) {
    var helpers = Chart.helpers;
    var eventPosition = helpers.getRelativePosition(e, this.chart);
    var elementsArray = [];

    var found = (function() {
        if (this.data.datasets) {
        for (var i = 0; i < this.data.datasets.length; i++) {
            if (helpers.isDatasetVisible(this.data.datasets[i])) {
            for (var j = 0; j < this.data.datasets[i].metaData.length; j++) {
                if (this.data.datasets[i].metaData[j].inLabelRange(eventPosition.x, eventPosition.y)) {
                return this.data.datasets[i].metaData[j];
                }
            }
            }
        }
        }
    }).call(this);

    if (!found) {
        return elementsArray;
    }

    helpers.each(this.data.datasets, function(dataset, dsIndex) {
        if (helpers.isDatasetVisible(dataset)) {
        elementsArray.push(dataset.metaData[found._index]);
        }
    });

    return elementsArray;
};

Chart.defaults.LineWithLine = Chart.defaults.line;
Chart.controllers.LineWithLine = Chart.controllers.line.extend({
   draw: function(ease) {
      Chart.controllers.line.prototype.draw.call(this, ease);

      if (this.chart.tooltip._active && this.chart.tooltip._active.length) {
         var activePoint = this.chart.tooltip._active[0],
             ctx = this.chart.ctx,
             x = activePoint.tooltipPosition().x,
             topY = this.chart.scales['y-axis-0'].top,
             bottomY = this.chart.scales['y-axis-0'].bottom;

         // draw line
         ctx.save();
         ctx.beginPath();
         ctx.moveTo(x, topY);
         ctx.lineTo(x, bottomY);
         ctx.lineWidth = 1;
         ctx.strokeStyle = '#bbb';
         ctx.stroke();
         ctx.restore();
      }
   }
});
