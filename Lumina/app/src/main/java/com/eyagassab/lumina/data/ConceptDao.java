package com.eyagassab.lumina.data;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;

import java.util.List;

@Dao
public interface ConceptDao {

    @Query("SELECT * FROM concepts ORDER BY id ASC")
    LiveData<List<Concept>> observeAllConcepts();

    @Query("SELECT * FROM concepts ORDER BY id ASC")
    List<Concept> getAllConceptsSync();

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertAll(List<Concept> concepts);

    @Query("SELECT COUNT(*) FROM concepts")
    int getCount();
}