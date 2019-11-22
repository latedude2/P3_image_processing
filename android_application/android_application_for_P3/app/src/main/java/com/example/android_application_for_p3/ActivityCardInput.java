package com.example.android_application_for_p3;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;

public class ActivityCardInput extends AppCompatActivity {

    ImageButton confirmButton;

    String handCards = "";

    String cards = "";
    String card1 = "";
    String card2 = "";

    String cardIndex = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_card_input);
        // setup the style to hide not needed bars and fill the background color
        new StyleSetup(this, getSupportActionBar());

        confirmButton = findViewById(R.id.confirm_button);
        confirmButton.setVisibility(View.GONE);

        if (getIntent().getStringExtra("cards") != null){
            Intent intentBefore = getIntent();
            cards = intentBefore.getStringExtra("cards");
            cardIndex = intentBefore.getStringExtra("cardIndex");
            if (cardIndex.equals("1")){
                card1 = cards;
                card2 = intentBefore.getStringExtra("card2");
                if(!card2.equals(""))
                    displayCard("2", card2);
                displayCard(cardIndex, card1);
                handCards = card1 + card2;
            } else if (cardIndex.equals("2")){
                card2 = cards;
                card1 = intentBefore.getStringExtra("card1");
                if(!card1.equals(""))
                    displayCard("1", card1);
                displayCard(cardIndex, card2);
                handCards = card1 + card2;
            }
        }

        if (handCards.length() == 4){
            confirmButton.setVisibility(View.VISIBLE);
        }
    }

    void displayCard(String cardIndex, String card){
        String viewName = "card" + cardIndex;
        int idOfView = getResources().getIdentifier(viewName, "id", getPackageName());
        ImageView imageView = findViewById(idOfView);
        int idOfImage = getResources().getIdentifier(card, "drawable", getPackageName());
        imageView.setImageResource(idOfImage);
    }

    public void onCardClick(View view){
        Intent intent = new Intent(this, ActivitySetSuits.class);
        String viewName = getResources().getResourceName(view.getId());
        cardIndex = String.valueOf(viewName.charAt(viewName.length()-1));
        intent.putExtra("cardIndex", cardIndex);
        intent.putExtra("card1", card1);
        intent.putExtra("card2", card2);
        startActivity(intent);
    }

    public void onConfirmClick(View view){
        Intent intent = new Intent(this, ActivitySpeedometer.class);
        intent.putExtra("handCards", handCards);
        startActivity(intent);
    }
}