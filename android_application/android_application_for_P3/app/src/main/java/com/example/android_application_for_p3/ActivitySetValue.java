package com.example.android_application_for_p3;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class ActivitySetValue extends AppCompatActivity {

    String card1 = ""; //card on the left
    String card2 = ""; //card on the right
    String cards = ""; //hand cards to send to the server (e.g. "5S8H", which is 5 of spades and 8 of hearts)
    String cardIndex = ""; //current index of the card (either 1 or 2)

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_set_value);
        // setup the style to hide not needed bars and fill the background color
        new StyleSetup(this, getSupportActionBar());

        // take the extras from the previous activity
        Intent intentBefore = getIntent();
        cards = intentBefore.getStringExtra("cards");
        card1 = intentBefore.getStringExtra("card1");
        card2 = intentBefore.getStringExtra("card2");
        cardIndex = intentBefore.getStringExtra("cardIndex");
    }

    public void onValueButtonClick(View view){
        //get the name of that button (e.g. "button_j")
        String buttonName = getResources().getResourceName(view.getId());
        //get the number of the button and add to what is now there
        cards += String.valueOf(buttonName.charAt(buttonName.length() - 1));

        Intent intent = new Intent(this, ActivityCardInput.class);
        //goes to the "select suit" activity
        intent.putExtra("cards", cards);
        intent.putExtra("card1", card1);
        intent.putExtra("card2", card2);
        intent.putExtra("cardIndex", cardIndex);
        startActivity(intent);
    }
}
