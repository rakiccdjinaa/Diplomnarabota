package com.cdss.heart;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@RestController
@CrossOrigin(origins = "*")
public class PredictionController {

    @PostMapping("/api/predict")
    public ResponseEntity<?> predict(@RequestBody Map<String, Object> userData) {
        try {
            RestTemplate restTemplate = new RestTemplate();
            String pythonApi = "http://127.0.0.1:5000/predict";


            System.out.println("Frontend data: " + userData);


            Object response = restTemplate.postForObject(pythonApi, userData, Object.class);

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body("Server error: " + e.getMessage());
        }
    }
}