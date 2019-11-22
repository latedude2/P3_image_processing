package com.example.android_application_for_p3;

import android.content.Intent;
import android.os.Bundle;

import android.view.View;

import androidx.appcompat.app.AppCompatActivity;


public class ActivitySetSuits extends AppCompatActivity {

    String card1 = "";
    String card2 = "";

    String card = ""; //hand cards to send to the server (e.g. "5S8H", which is 5 of spades and 8 of hearts)
    String cardIndex = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_set_suits);

        // setup the style to hide not needed bars and fill the background color
        new StyleSetup(this, getSupportActionBar());

        if (getIntent() != null){
            cardIndex = getIntent().getStringExtra("cardIndex");
            card1 = getIntent().getStringExtra("card1");
            card2 = getIntent().getStringExtra("card2");
        }
    }

    public void onSuitClick(View view){
        //get the name of that button (e.g. "button_1")
        String buttonName = getResources().getResourceName(view.getId());
        //get the number of the button

        Intent intent = new Intent(this, ActivitySetValue.class);
        intent.putExtra("cardIndex", cardIndex);
        intent.putExtra("card1", card1);
        intent.putExtra("card2", card2);
        intent.putExtra("cards", String.valueOf(buttonName.charAt(buttonName.length() - 1)));
        startActivity(intent);
    }
}
