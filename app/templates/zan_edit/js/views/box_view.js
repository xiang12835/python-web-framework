

var BoxView = Backbone.View.extend({

    //... is a list tag.
    tagName:  "li",

    // Cache the template function for a single item.
    template: _.template($('#box-template').html()),

    // The DOM events specific to an item.
    // events: {
    //   "click .app-carousel"   : "toggleDone",
    //   "dblclick .view"  : "edit",
    // },

    initialize: function() {
      //this.listenTo(this.model, 'change', this.render);
      //this.listenTo(this.model, 'destroy', this.remove);
    },

    // Re-render the titles of the todo item.
    render: function() {
      var default_url = "http://r3.ykimg.com/05100000557EF64A6714C071A70CDCBF";
      var default_title = "视频标题";
      var default_summary = "腰封";
      var default_subtitle = "副标题";
      var _form = "box_form";
      var _id= "module_"+sort_index;
      var box_id="video_box_"+sort_index;
      var data = {"form":_form,"type":TYPE_BOX,"id":_id,"sort":sort_index,"box_id":box_id};
      var templates = this.template(data);
      var boxItemView = new BoxItemView;

      //console.log(templates);

      $("#sortable").append(templates);
      $('#'+box_id).append(boxItemView.render(default_url,default_title,default_summary,default_subtitle));
      $('#'+box_id).append(boxItemView.render(default_url,default_title,default_summary,default_subtitle));

      /*move side bar*/
      var pos = $("#"+_id).position();
      $("#app-sidebar").animate({ 'top': pos.top + 'px'}, 200, function(){});
      current_index = sort_index;
      /*add to struct*/
      var boxModel = new BoxModel;
      dataList.add(boxModel);
      var nowList= dataList.get_index(sort_index)
      nowList.set('box_id',box_id);
      init_module(dataList.get_index(sort_index),sort_index,_id,"视频盒子");
      init_form(_form)
      change_form(_form);
      sort_index++;
    },

    // Remove the item, destroy the model.
    remove: function() {
      this.model.destroy();
    }

  });
