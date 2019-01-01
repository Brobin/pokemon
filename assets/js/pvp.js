
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

    var mons = Object.keys(pokemon);
    var types = Object.keys(type_map);
    mons.sort()
    types.sort()

    self.mons = ko.observableArray(mons);
    self.types = ko.observableArray(types);

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
        return effective;
    }

    self.chargeEffective = function(){
        var c1 = self.effective(self.charge1());
        var c2 = self.effective(self.charge2());
        ko.utils.arrayForEach(c2, function(c){
            if(c1.indexOf(c) == -1) {
                c1.push(c);
            }
        });
        return c1;
    }

    self.chargeEffectiveImages = ko.computed(function(){
        return self.images(self.chargeEffective());
    });

    self.resists = ko.computed(function(){
        var effective = [];
        var type1 = pokemon[self.name()][0];
        var type2 = pokemon[self.name()][1];
        ko.utils.arrayForEach(Object.keys(type_map), function(type){
            var effectiveness = type_map[type][type1] * type_map[type][type2];
            if (effectiveness < 1) {
                effective.push(type);
            }
        });
        return self.images(effective);
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
