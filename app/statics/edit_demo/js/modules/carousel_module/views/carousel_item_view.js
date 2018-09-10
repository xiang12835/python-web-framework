var CarousulItemView = Backbone.View.extend({

    tagName: "div",

    // Cache the template function for a single item.
    template: _.template($('#carousel-item-template').html()),



    initialize: function () {
        
    },

    // Re-render the titles of the todo item.
    render: function (_url,_title) {
        var data = {
          "item_img":_url,
          "item_title":_title
      };
        var templates = this.template(data);

        return templates;
        
    },

    // Remove the item, destroy the model.
    remove: function () {
        this.model.destroy();
    }

});
