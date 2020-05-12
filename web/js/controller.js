
function loadPersons ( selectObj ) {
    var url = "/api/persons";

    $.ajax({
        url: url,
        type: "get",
        accept: "application/json",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
            selectObj.empty();
            var option = $("<option value=''>-choose person-</option>");
            selectObj.append(option);
            result = data["result"];
            for(i in result){
                item = result[i];
                var option = $("<option value='"+item['person_id']+"'>"+item['person_name']+"</option>");
                selectObj.append(option);
            }
        },
        error: function(jqXHR,textStatus,errorThrown) {
            console.log('fail--->', textStatus);
        }
    });
}

function loadGroups( selectObj ) {
    var url = "/api/groups";
    $.ajax({
        url: url,
        type: "get",
        accept: "application/json",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
            selectObj.empty();
            var option = $("<option value=''>-choose group-</option>");
            selectObj.append(option);
            result = data["result"];
            for(i in result){
                item = result[i];
                var option = $("<option value='"+item['group_id']+"'>"+item['group_name']+"</option>");
                selectObj.append(option);
            }
        },
        error: function(jqXHR,textStatus,errorThrown) {
            console.log('fail--->', textStatus);
        }
    });
}

function allowRoles() {

    if($("#allow #group_id").has('option').length < 1){
        alert('please load Roles!');
    } else if($("#allow #person_id").has('option').length < 1){
        alert('please load Persons!');
    } else if($("#allow #group_id").val() == ""){
        alert('please choose a Role!');
    } else if($("#allow #person_id").val() == ""){
        alert('please choose a Person!');
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
}

function submitGroup(){
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
}

function submitPerson() {
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
}

function identify() {
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

        $.ajax({
            url: url,
            type: "post",
            accept: "application/json",
            contentType: "application/json; charset=utf-8",
            data: json_str,
            dataType: "json",
            success: function(data) {
                console.log('success--->', data);
                if (data["result"]) {
                    object_list = data["object_id_list"];
                    result = "<ul>"

                    nearest = 1;
                    for(i in object_list){
                        object = object_list[i];
                        oid = object['object_id'];
                        distance = Number(object['distance']);
                        var li = "<li>"+oid+" : "+distance+"</li>";
                        result += li;
                        console.log('distance--->', distance);
                        if(distance < nearest) {
                            nearest = distance;
                        }
                    }
                    verifyAndOpen(nearest);
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
}

var deviceCallback = {"result":""};

var deviceSocket = null;

function setDeviceSocket(socketAddr){
    deviceSocket = new WebSocket(socketAddr);
    deviceSocket.onmessage  = function(message){
        console.log("ws message--->",message.data);
        if(message.data === "OK") {
            openToast("The door is opened!");
        }
    };
}

function verifyAndOpen(distance) {
    if(distance < 0.5){
        openDevice();
    }
}

function openDevice() {
    deviceSocket.send("OPEN");
}

function openToast(msg) {
    console.log("toast message--->",msg);
    $("#toast-message").text(msg);
    $("#main-toast").toast('show');
}
