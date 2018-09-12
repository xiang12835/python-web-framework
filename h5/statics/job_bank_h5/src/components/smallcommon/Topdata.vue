<template>
   <div class="zone-bd" id="page-data">
    <div class="bd-items">
        <div><em class="em">{{lnum}}</em>个</div>
        <div>正在报名的职位</div>
    </div>
    <div class="bd-items">
        <div><em class="em">{{cnum}}</em>个</div>
        <div>招考职位</div>
    </div>
    <div class="bd-items">
        <div><em class="em">{{rnum}}</em>个</div>
        <div>近7日新增职位</div>
    </div>
</div>
</template>

<script>
import { api_get_somenum} from "../../networks/others"
export default {
    name: 'HelloWorld',
    data () {
        return {
            lnum: '',
            cnum: '',
            rnum: '',
        }
    },
    created: function() {
        var context=this;
        var promise = api_get_somenum(context);
        promise.then(function(res) {
            console.log(res);
            context.lnum=res.data.data.total;
            context.cnum=res.data.data.current_data;
            context.rnum=res.data.data.data_update;
           
        }).catch(function(error){
            console.error(error);
        });
    },
    methods: {
    
    }

}
</script>


<style scoped>
 .zone-bd {
    padding: 11px 0;
    font-size: 12px;
    position: relative;
     display: flex;
    justify-content: space-around;
    align-items: center;
    color: #a5a4a4;
}
.zone-bd .bd-items{
    flex: 1;
    text-align: center;
}


.zone-bd .bd-items .em {
    font-size: 16px;
    color: #f1514e;
    margin-right:5px;
}

.zone-bd:after {
    position: absolute;
    bottom: 0;
    left: 3%;
    content: "";
    display: block;
    width: 94%;
    height: 1px;
    background: #f1f4f6;
}
em, i {
    font-style: normal;
}



</style>
