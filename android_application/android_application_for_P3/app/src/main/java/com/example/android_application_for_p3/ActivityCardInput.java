package com.example.android_application_for_p3;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

public class ActivityCardInput extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_card_input);

        // setup the style to hide not needed bars and fill the background color
        new StyleSetup(this, getSupportActionBar());


    }
}
