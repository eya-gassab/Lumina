package com.eyagassab.lumina.data.remote;

import com.google.gson.annotations.SerializedName;

public class ConceptDto {

    @SerializedName("id")
    private int id;

    @SerializedName("title")
    private String title;

    @SerializedName("category")
    private String category;

    @SerializedName("tldr")
    private String tldr;

    @SerializedName("explanation")
    private String explanation;

    @SerializedName("practical_application")
    private String practicalApplication;

    public int getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getCategory() {
        return category;
    }

    public String getTldr() {
        return tldr;
    }

    public String getExplanation() {
        return explanation;
    }

    public String getPracticalApplication() {
        return practicalApplication;
    }
}