package com.example.android_application_for_p3;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;

public class ActivitySpeedometer extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        try {
            getSupportActionBar().hide();
        } catch (Exception e){
            System.out.println("No action bar found to hide");
        }
        Intent previousActivity = getIntent(); // use for taking the info to here
    }
}
