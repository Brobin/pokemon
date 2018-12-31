
function PvPViewModel() {
    var self = this;
    self.pokemon = ko.observableArray([]);

    self.mons = ko.observableArray(Object.keys(pokemon));
    self.types = ko.observableArray(Object.keys(type_map));
}

function Pokemon(name, charge1, charge2) {
    var self = this;
    self.name = ko.observable(name);
    self.charge1 = ko.observable(charge1);
    self.charge2 = ko.observable(charge2);

    self.mons = ko.observableArray(Object.keys(pokemon));
    self.types = ko.observableArray(Object.keys(type_map));

    self.images = function(types){
        var result = '';
        ko.utils.arrayForEach(types, function(type){
            result = result + '<div class="type-icon"><img src="/static/img/types/'+type+'.png"/></div>'
        });
        return result;
    }

    self.effective = function(type){
        var effective = [];
        ko.utils.arrayForEach(Object.keys(type_map[type]), function(key){
            if (type_map[type][key] > 1) {
                effective.push(key)
            }
        });
        return self.images(effective);
    }

    self.charge1Effective = ko.computed(function(){
        return self.effective(self.charge1());
    });

    self.charge2Effective = ko.computed(function(){
        return self.effective(self.charge2());
    });

    self.vulnerable = ko.computed(function(){
        var effective = [];
        var type1 = pokemon[self.name()][0];
        var type2 = pokemon[self.name()][1];
        ko.utils.arrayForEach(Object.keys(type_map), function(type){
            var effectiveness = type_map[type][type1] * type_map[type][type2];
            if (effectiveness > 1) {
                effective.push(type);
            }
        });
        return self.images(effective);
    });
}
