
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
    self.chart = chart;
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

    self.chartData = ko.computed(function() {
        var x = self.logs().map(function(log){return log.created});
        return [{
            x: x,
            y: self.logs().map(function(log){return log.mystic}),
            type: 'scatter',
            name: 'Mystic',
            marker: {
                color: '#3366cc'
            }
        },{
            x: x,
            y: self.logs().map(function(log){return log.valor}),
            type: 'scatter',
            name: 'Valor',
            marker: {
                color: '#dc3912'
            }
        },{
            x: x,
            y: self.logs().map(function(log){return log.instinct}),
            type: 'scatter',
            name: 'Instinct',
            marker: {
                color: '#ff9900'
            }
        }];
    });
}
