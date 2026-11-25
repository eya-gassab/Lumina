package com.eyagassab.lumina.data;

import android.content.Context;

import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;

@Database(entities = {Concept.class}, version = 1, exportSchema = false)
public abstract class LuminaDatabase extends RoomDatabase {

    private static volatile LuminaDatabase instance;

    public abstract ConceptDao conceptDao();

    public static LuminaDatabase getInstance(Context context) {
        if (instance == null) {
            synchronized (LuminaDatabase.class) {
                if (instance == null) {
                    instance = Room.databaseBuilder(
                            context.getApplicationContext(),
                            LuminaDatabase.class,
                            "lumina_database"
                    ).build();
                }
            }
        }
        return instance;
    }
}