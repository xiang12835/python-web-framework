var CarousulItemView = Backbone.View.extend({

    //... is a list tag.
    tagName: "div",

    // Cache the template function for a single item.
    template: _.template($('#carousel-item-template').html()),

    // The DOM events specific to an item.
    // events: {
    //   "click .app-carousel"   : "toggleDone",
    //   "dblclick .view"  : "edit",
    // },

    initialize: function () {
        //this.listenTo(this.model, 'change', this.render);
        //this.listenTo(this.model, 'destroy', this.remove);
    },

    // Re-render the titles of the todo item.
    render: function (_url,_title) {
        var data = {
          "item_img":_url,
          "item_title":_title
      };
        var templates = this.template(data);

        //console.log(templates);

        return templates;
        /*move side bar*/
        //var pos = $("#" + _id).position();
        //$("#app-sidebar").animate({ 'top': pos.top + 'px'}, 200, function () {
        //});
        //init_from(_form)
        //change_form(_form);
        //current_index = sort_index;
        /*add to struct*/
        //var boxModel = new BoxModel;
        //dataList.add(boxModel);
        //init_module(dataList.get_index(sort_index), sort_index, _id);
        //sort_index++;
    },

    // Remove the item, destroy the model.
    remove: function () {
        this.model.destroy();
    }

});
