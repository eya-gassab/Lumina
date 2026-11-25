package com.eyagassab.lumina;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

import com.eyagassab.lumina.data.remote.ConceptDto;
import com.eyagassab.lumina.data.remote.DailyConceptsResponseDto;
import com.google.gson.Gson;

import org.junit.Test;

public class JsonMappingTest {

    @Test
    public void dailyConceptsJson_mapsAllFieldsCorrectly() {
        String sampleJson = "{"
                + "\"date\": \"2026-11-25\","
                + "\"count\": 1,"
                + "\"concepts\": [{"
                + "  \"id\": 1,"
                + "  \"title\": \"Le Rasoir d'Ockham\","
                + "  \"category\": \"Prise de décision\","
                + "  \"tldr\": \"L'explication la plus simple est souvent la meilleure.\","
                + "  \"explanation\": \"Formulé par Guillaume d'Ockham...\","
                + "  \"practical_application\": \"Vérifie d'abord la cause la plus simple.\""
                + "}]"
                + "}";

        DailyConceptsResponseDto response = new Gson().fromJson(sampleJson, DailyConceptsResponseDto.class);

        assertNotNull(response);
        assertEquals("2026-11-25", response.getDate());
        assertEquals(1, response.getCount());
        assertNotNull(response.getConcepts());
        assertEquals(1, response.getConcepts().size());

        ConceptDto first = response.getConcepts().get(0);
        assertEquals(1, first.getId());
        assertEquals("Le Rasoir d'Ockham", first.getTitle());
        assertEquals("Prise de décision", first.getCategory());
        assertEquals("L'explication la plus simple est souvent la meilleure.", first.getTldr());
        assertEquals("Vérifie d'abord la cause la plus simple.", first.getPracticalApplication());
    }
}