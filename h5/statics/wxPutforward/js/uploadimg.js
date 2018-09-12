!function(e) {
    var i = e.URL || e.webkitURL
      , s = {
        init: function(e) {
            this.formArea = $(e.id),
            this.box = e.box,
            this.bindFuns(),
            this.compressHeight = e.compressHeight,
            this.compressHeight && this.formArea.append($('<canvas id="img-canvas" style="display:none;"></canvas>'))
        },
        bindFuns: function() {
            var t, a = this;
            s.formArea.find("input[type=file]").on("compress", function(e) {
                a.isCompress = e._args,
                t = $(this).parents(a.box).find(".imgShow"),
                a.getDataURL(this, t)
            })
        },
        getDataURL: function(e, t) {
            var a = this;
            if (i && e.files)
                dataURL = i.createObjectURL(e.files[0]),
                a.setPicPath(t, dataURL);
            else if ("undefined" != typeof FileReader && e.files)
                reader = new FileReader,
                reader.onload = function(e) {
                    dataURL = e.target.result,
                    a.setPicPath(t, dataURL)
                }
                ,
                reader.readAsDataURL(e.files[0]);
            else
                try {
                    me.select(),
                    top.parent.document.body.focus(),
                    srcText = document.selection.createRange().text,
                    document.selection.empty(),
                    a.setPicPath(e, t, srcText)
                } catch (e) {}
        },
        setPicPath: function(e, t) {
            if (e.attr("_src", t),
            e.parent().find(".icon-upload, .des").css("opacity", 0),
            i || "undefined" != typeof FileReader)
                this.canvasRander(e, t, this.isCompress);
            else {
                var a = e.parents(".filter")[0];
                e.hide();
                try {
                    a.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale)",
                    a.filters.item("DXImageTransform.Microsoft.AlphaImageLoader").src = t
                } catch (e) {}
                a.style.display = "block"
            }
        },
        canvasRander: function(a, e, i) {
            var s, n = this.compressHeight, r = new Image;
            r.onload = function() {
                var e = document.getElementById("img-canvas");
                i && r.height > n && (r.width *= n / r.height,
                r.height = n);
                var t = e.getContext("2d");
                t.clearRect(0, 0, e.width, e.height),
                e.width = r.width,
                e.height = r.height,
                t.drawImage(r, 0, 0, r.width, r.height),
                s = e.toDataURL("image/jpeg"),
                a.attr("src", s).show()
            }
            ,
            r.src = e
        },
        inputFileReset: function(e) {
            var t = $(e).parents(s.box)
              , a = document.createElement("form")
              , i = t.find(".filename");
            i.before(a),
            $(a).append(i),
            a.reset(),
            $(a).after(i),
            $(a).remove()
        }
    };
    e.uploadImg = s
}(window);
