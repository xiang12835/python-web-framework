

var CarouselView = Backbone.View.extend({

    //... is a list tag.
    tagName:  "li",

    // Cache the template function for a single item.
    template: _.template($('#carousel-template').html()),

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
      var default_title = "轮播图"
      var _form = "carousel_form";
      var _id= "module_"+sort_index;
      var carousel_id="carousel_"+sort_index;
      var carousulItemView = new CarousulItemView;

      var data = {
          "form":_form,
          "type":TYPE_CAROUSEL,
          "id":_id,
          "sort":sort_index,
          "carousel_id":carousel_id
      };
      var templates = this.template(data);

      //console.log(templates);

      $("#sortable").append(templates);
      $('#'+carousel_id).slick({
                dots: true,
                autoplay: true,
                autoplaySpeed: 5000,
                infinite: true,
                speed: 700,
                cssEase: 'linear',
                arrows: false
      });
      //add two default slick
      $('#'+carousel_id).slick('slickAdd',carousulItemView.render(default_url,default_title));
      $('#'+carousel_id).slick('slickAdd',carousulItemView.render(default_url,default_title));

      /*move side bar*/
      var pos = $("#"+_id).position();
      $("#app-sidebar").animate({ 'top': pos.top + 'px'}, 200, function(){});
      current_index = sort_index;
      /*add to struct*/
      var icollection = new CarouselCollection;
      dataList.add(icollection);
      var nowList= dataList.get_index(sort_index)
      nowList.set('carousel_id',carousel_id);
      init_module(nowList,sort_index,_id,"轮播图");
      init_form(_form)
      change_form(_form);
      sort_index++;
    },

    // Remove the item, destroy the model.
    remove: function() {
      this.model.destroy();
    }

  });
