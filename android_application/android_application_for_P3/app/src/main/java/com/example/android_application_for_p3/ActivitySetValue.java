package com.example.android_application_for_p3;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class ActivitySetValue extends AppCompatActivity {

    String handCards = ""; //hand cards to send to the server (e.g. "5S8H", which is 5 of spades and 8 of hearts)

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_set_value);

        // setup the style to hide not needed bars and fill the background color
        new StyleSetup(this, getSupportActionBar());

        // if it was made from the intent (another activity called it), then take the info about handCards
        if (getIntent() != null){
            Intent intentBefore = getIntent();
            handCards = intentBefore.getStringExtra("handCards");
        }

    }
    public void onValueButtonClick(View view){
        //get the name of that button (e.g. "button_1")
        String buttonName = getResources().getResourceName(view.getId());
        //get the number of the button
        String value = String.valueOf(buttonName.charAt(buttonName.length() - 1));
        if (handCards == null)
            handCards = value;
        else
            handCards += value;
        //goes to the "select suit" activity
        startActivity(
                new Intent(this, ActivitySetSuits.class)
                        .putExtra("handCards", handCards)
        );
    }
}
