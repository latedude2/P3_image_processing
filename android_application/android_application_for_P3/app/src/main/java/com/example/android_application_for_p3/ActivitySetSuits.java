package com.example.android_application_for_p3;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

import android.view.View;


public class ActivitySetSuits extends Activity {

    String handCards = ""; //hand cards to send to the server (e.g. "5S8H", which is 5 of spades and 8 of hearts)

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_set_suits);
        handCards = getIntent().getStringExtra("handCards"); // take the string from the previous activity
    }

    public void onSuitClick(View view){
        //get the name of that button (e.g. "button_1")
        String buttonName = getResources().getResourceName(view.getId());
        //get the number of the button
        String value = String.valueOf(buttonName.charAt(buttonName.length() - 1));
        handCards = handCards + value;

        if (handCards.length() == 4) {
            Intent intent = new Intent(this, ActivitySpeedometer.class);
            intent.putExtra("handCards", handCards);
            startActivity(intent);
        } else {
            //goes to the "select suit" activity
            Intent intent = new Intent(this, MainActivity.class);
            intent.putExtra("handCards", handCards);
            startActivity(intent);
        }
    }

}
