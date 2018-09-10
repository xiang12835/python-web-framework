/* model */

var HeadModel = Backbone.Model.extend({
    defaults: {
        type: "head",
        title: "微页面标题",
        module_sort: 0,
        module_id:'module_0'
    }
});

var CarouselModel = Backbone.RelationalModel.extend({
    defaults: {
        type: "carousel",
        title: "",
        video_link: "",
        image_url: "",
        item_id:"",
        sort: 0
    }
});

var CarouselCollection = Backbone.RelationalModel.extend({

    defaults: {
        type: "carousels",
        title: "",
        module_sort: 1,
        module_id:"",
        carousel_id:"",
        items:[]
    }
});


var VideoModel = Backbone.RelationalModel.extend({
    defaults: {
        type: "video",
        summary: "",
        image_url: "",
        title: "",
        video_link:"",
        sub_title: "",
        item_id:"",
        sort: 0
    }
});

var BoxModel = Backbone.RelationalModel.extend({

    defaults: {
        type: "box",
        title: "",
        title_link: "",
        module_sort: 2,
        module_id:"",
        box_id:"",
        items:[]
    }
});


var DataStructList = Backbone.Model.extend({
    defaults: {
        data: []
    },

    add: function (obj) {
        this.get("data").push(obj);
    },
    get_index: function (i) {
        return this.get("data")[i];
    },
    get_id: function (_id) {
        var now_data = this.get("data")
        for(var i=0;i<this.len(0);i++ ){
            if( now_data[i].get("module_id")==_id){
                return now_data[i]
            }
        }
    },
    len: function (i) {
        return this.get("data").length;
    },
    my_sort: function(){
        this.get("data").sort(function(a,b){
            return a.get('module_sort')- b.get('module_sort')
        })
    }
});


function debug_log(obj) {
    console.log(JSON.stringify(obj.toJSON(), null, 4));
}

function init_module(obj,_sort,_id,_name){
    obj.set('module_sort',_sort);
    obj.set('module_id',_id);
    obj.set('items',[]);
    obj.set('title',_name+_sort)
    debug_log(dataList)
}

var defaultHead = new HeadModel;
var dataList = new DataStructList;
dataList.add(defaultHead);




