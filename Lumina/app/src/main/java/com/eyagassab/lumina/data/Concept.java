package com.eyagassab.lumina.data;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "concepts")
public class Concept {

    @PrimaryKey
    private final int id;
    private final String title;
    private final String tldr;
    private final String practice;

    public Concept(int id, String title, String tldr, String practice) {
        this.id = id;
        this.title = title;
        this.tldr = tldr;
        this.practice = practice;
    }

    public int getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getTldr() {
        return tldr;
    }

    public String getPractice() {
        return practice;
    }
}