
$("#load_persons").click(function( event ) {
    var url = "/api/persons";

    $.ajax({
        url: url,
        type: "get",
        accept: "application/json",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
            $("#allow #person_id").empty();
            var option = $("<option value=''>-choose person-</option>");
            $("#allow #person_id").append(option);
            result = data["result"];
            for(i in result){
                item = result[i];
                var option = $("<option value='"+item['person_id']+"'>"+item['person_name']+"</option>");
                $("#allow #person_id").append(option);
            }
        },
        error: function(jqXHR,textStatus,errorThrown) {
            console.log('fail--->', textStatus);
        }
    });
});

$("#load_groups").click(function( event ) {
    var url = "/api/groups";
    $.ajax({
        url: url,
        type: "get",
        accept: "application/json",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
            $("#allow #group_id").empty();
            var option = $("<option value=''>-choose group-</option>");
            $("#allow #group_id").append(option);
            result = data["result"];
            for(i in result){
                item = result[i];
                var option = $("<option value='"+item['group_id']+"'>"+item['group_name']+"</option>");
                $("#allow #group_id").append(option);
            }
        },
        error: function(jqXHR,textStatus,errorThrown) {
            console.log('fail--->', textStatus);
        }
    });
});

$("#load_identify_groups").click(function( event ) {
    var url = "/api/groups";
    $.ajax({
        url: url,
        type: "get",
        accept: "application/json",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
            $("#identify #group_id").empty();
            var option = $("<option value=''>-choose group-</option>");
            $("#identify #group_id").append(option);
            result = data["result"];
            for(i in result){
                item = result[i];
                var option = $("<option value='"+item['group_id']+"'>"+item['group_name']+"</option>");
                $("#identify #group_id").append(option);
            }
        },
        error: function(jqXHR,textStatus,errorThrown) {
            console.log('fail--->', textStatus);
        }
    });
});

$("#submit_allow").click(function( event ) {
    event.preventDefault();

    if($("#allow #person_id").val() == ""){
        alert('please choose a Person!');
    }else if($("#allow #group_id").val() == ""){
        alert('please choose a Role!');
    } else {
        var url = "/api/group";
        var data = $("form#group").serializeArray();

        var object = {};
        for (var i = 0; i < data.length; i++){
            object[data[i]['name']] = data[i]['value'];
        }
        
        var json_str = JSON.stringify(object);

        $.ajax({
            url: url,
            type: "post",
            accept: "application/json",
            contentType: "application/json; charset=utf-8",
            data: json_str,
            dataType: "json",
            success: function(data) {
                console.log('success--->', data);
            },
            error: function(jqXHR,textStatus,errorThrown) {
                console.log('fail--->', textStatus);
            }
        });
    }
});

$("#submit_group").click(function( event ) {
    event.preventDefault();

    if($("#group #group_id").val() == ""){
        alert('please input Group ID!');
    } else {
        var url = "/api/group";
        
        object["group_id"] = $("#group #group_id").val();
        object["group_name"] = $("#group #group_name").val();
        
        var json_str = JSON.stringify(object);

        $.ajax({
            url: url,
            type: "post",
            accept: "application/json",
            contentType: "application/json; charset=utf-8",
            data: json_str,
            dataType: "json",
            success: function(data) {
                console.log('success--->', data);
            },
            error: function(jqXHR,textStatus,errorThrown) {
                console.log('fail--->', textStatus);
            }
        });
    }
});

$("#submit_face").click(function( event ) {
    event.preventDefault();
    if($("#face #person_id").val() == ""){
        alert('please input Person ID!');
    } else if($("#face #img").val() == ""){
        alert('please attach Image File!');
    } else {
        var url = "/api/person";
        var data = $("form#face").serializeArray();

        console.log("data", data);

        var file = document.querySelector('#face #img');
        var fileList = file.files ;
        var reader = new FileReader();
        reader.readAsDataURL(fileList[0]);
        
        reader.onload = function() {
            var base64data = reader.result;
            var img_result = base64data.split(',')[1]

            // console.log("data", data);
            data.push({"name":"img", "value":img_result});

            // json object to json string
            var object = {};
            for (var i = 0; i < data.length; i++){
                object[data[i]['name']] = data[i]['value'];
            }
            
            var json_str = JSON.stringify(object);

            $.ajax({
                url: url,
                type: "post",
                accept: "application/json",
                contentType: "application/json; charset=utf-8",
                data: json_str,
                dataType: "json",
                success: function(data) {
                    console.log('success--->', data);
                },
                error: function(jqXHR,textStatus,errorThrown) {
                    console.log('fail--->', textStatus);
                }
            });
        }
    }
});

$("#submit_identify").click(function( event ) {
    event.preventDefault();
    if($("#identify #group_id").has('option').length < 1){
        alert('please load Roles!');
    } else if($("#identify #group_id").val() == ""){
        alert('please choose a Role!');
    } else {

        var canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d')
            .drawImage(video, 0, 0, canvas.width, canvas.height);

        var url = "/api/identify";

        var object = {};
        object["group_id"] = $("#identify #group_id").val()

        object["img"] = canvas.toDataURL().split(',')[1];

        var json_str = JSON.stringify(object);

        // console.log('json_string', json_str)

        $.ajax({
            url: url,
            type: "post",
            accept: "application/json",
            contentType: "application/json; charset=utf-8",
            data: json_str,
            dataType: "json",
            success: function(data) {
                console.log('success--->', data);
                result = data["result"];
                if (result) {
                    object_list = data["object_id_list"];
                    result = "<ul>"
                    for(i in object_list){
                        object = object_list[i];
                        var li = "<li>"+object['object_id']+" : "+object['distance']+"</li>";
                        result += li;
                    }
                    result += "</ul>";
                    $("#result_face").html(result);
                } else {
                    $("#result_face").html(data["description"]);
                }
            },
            error: function(jqXHR,textStatus,errorThrown) {
                console.log('fail--->', textStatus);
            }
        });

    }
});
