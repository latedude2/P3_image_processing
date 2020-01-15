package com.example.android_application_for_p3.view;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import androidx.appcompat.app.AppCompatActivity;

import com.example.android_application_for_p3.R;

public class ActivitySetSuits extends AppCompatActivity {

    String card1 = "";
    String card2 = "";
    String cardIndex = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_set_suits);

        // setup the style to hide not needed bars and fill the background color
        new StyleSetup(this, getSupportActionBar());

        //get the Extras from the previous activity
        cardIndex = getIntent().getStringExtra("cardIndex");
        card1 = getIntent().getStringExtra("card1");
        card2 = getIntent().getStringExtra("card2");
    }

    public void onSuitClick(View view){
        Intent intent = new Intent(this, ActivitySetValue.class);
        intent.putExtra("cardIndex", cardIndex); //current card taken
        intent.putExtra("card1", card1);
        intent.putExtra("card2", card2);

        //get the name of that button (e.g. "suith", which is suit button for hearts)
        String buttonName = getResources().getResourceName(view.getId());
        //get the number of the button and send the last letter, because at first it's always empty
        intent.putExtra("cards", String.valueOf(
                buttonName.charAt(buttonName.length() - 1)));
        startActivity(intent);
    }
}
