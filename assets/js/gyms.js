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

function GymLog(created, mystic, valor, instinct) {
    var self = this;
    self.created = created;
    self.mystic = mystic;
    self.valor = valor;
    self.instinct = instinct;

    self.time = ko.computed(function(){
        return moment(self.created).format('MMM D, YYYY, h:mm a');
    });
}


function GymViewModel() {
    var self = this;
    self.gymLogs = ko.observableArray([]);
    self.filter = ko.observable(1);

    self.filterDate = ko.computed(function() {
        var date = new Date();
        date.setDate(date.getDate() - self.filter());
        return date;
    });

    self.logs = ko.computed(function() {
        var date = self.filterDate();
        return ko.utils.arrayFilter(self.gymLogs(), function(log){
            return log.created >= date;
        });
    });

    self.recent = ko.computed(function(){
        var date = new Date();
        date.setHours(date.getHours() - 3);
        return ko.utils.arrayFilter(self.gymLogs(), function(log){
            return log.created >= date;
        });
    });

    self.min = function(attr) {
        var min = 250;
        ko.utils.arrayForEach(self.logs(), function(log){
            min = log[attr] < min ? log[attr] : min;
        });
        return min;
    }

    self.max = function(attr) {
        var max = 0;
        ko.utils.arrayForEach(self.logs(), function(log){
            max = log[attr] > max ? log[attr] : max;
        });
        return max;
    }

    self.avg = function(attr) {
        var team = 0;
        var total = 0;
        ko.utils.arrayForEach(self.logs(), function(log){
            total += log.mystic + log.valor + log.instinct;
            team += log[attr];
        });
        return (team / total * 100).toFixed(2) + "%";
    }
    
    self.minMystic = ko.computed(function(){return self.min('mystic')});
    self.maxMystic = ko.computed(function(){return self.max('mystic')});
    self.avgMystic = ko.computed(function(){return self.avg('mystic')});
    self.minValor = ko.computed(function(){return self.min('valor')});
    self.maxValor = ko.computed(function(){return self.max('valor')});
    self.avgValor = ko.computed(function(){return self.avg('valor')});
    self.minInstinct = ko.computed(function(){return self.min('instinct')});
    self.maxInstinct = ko.computed(function(){return self.max('instinct')});
    self.avgInstinct = ko.computed(function(){return self.avg('instinct')});

    self.labels = ko.computed(function(){
        return self.logs().map(function(log){return log.created});
    });

    self.chartData = ko.computed(function() {
        return [{
            label: 'Mystic',
            data: self.logs().map(function(log){return log.mystic}),
            backgroundColor: "rgb(54, 162, 235)",
            borderColor: "rgb(54, 162, 235)",
            fill: false,
        },{
            label: 'Valor',
            data: self.logs().map(function(log){return log.valor}),
            backgroundColor: "rgb(255, 99, 132)",
            borderColor: "rgb(255, 99, 132)",
            fill: false,
        },{
            label: 'Instinct',
            data: self.logs().map(function(log){return log.instinct}),
            backgroundColor: "rgb(255, 205, 86)",
            borderColor: "rgb(255, 205, 86)",
            fill: false,
        }];
    });
}
