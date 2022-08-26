function config_set_time_to_computer_time()
{
    //Get current DateTime
    var d = new Date();
    console.log("Current Date: ", d);
}

function config_post_data_to_server()
{
    //Post data to server
    console.log("config_post_data_to_server");

    //get the values from the form
    var accelerometer_precision = $("#accelerometer_precision_select").val();
    var gyrometer_precision = $("#gyrometer_precision_select").val();
    var imu_sampling_rate = $("#imu_sampling_rate_select").val();
    var adc_sampling_rate = $("#adc_sampling_rate_select").val();

    //post the values to the server
    $.post("/config_update", {
        accelerometer_precision: accelerometer_precision,
        gyrometer_precision: gyrometer_precision,
        imu_sampling_rate: imu_sampling_rate,
        adc_sampling_rate: adc_sampling_rate
        }, function(data, status){
            console.log("Data: " + data + "\nStatus: " + status);
        }
    );
}