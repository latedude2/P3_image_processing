package com.example.android_application_for_p3;

import androidx.appcompat.app.ActionBar;
import android.view.View;

import androidx.appcompat.app.AppCompatActivity;

class StyleSetup {

    StyleSetup(AppCompatActivity activity, ActionBar actionBar){
        setup(activity, actionBar);
    }

    private void setup(AppCompatActivity activity, ActionBar actionBar){
        try {
            actionBar.hide();
            View decorView = activity.getWindow().getDecorView();
            int uiOptions = View.SYSTEM_UI_FLAG_FULLSCREEN;
            decorView.setSystemUiVisibility(uiOptions);
            activity.getActionBar().hide();
            activity.setTheme(R.style.AppTheme);
        } catch (Exception e){ System.out.println("No action bar found to hide"); }
    }
}
