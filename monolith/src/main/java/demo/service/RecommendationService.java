/* Copyright 2020 Google LLC. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package demo.service;

import demo.model.Product;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import java.util.ArrayList;
import java.util.Collections;

@Service
public class RecommendationService {

  @Autowired private ProductService productService;

  private final RestTemplate restTemplate = new RestTemplate();
  
  @Value("${recommendation.service.url}")
  private String recommendationServiceUrl;

  @Value("${recommendation.service.port}")
  private String recommendationServicePort;

  /**
   * Get recommended products list based on user selection
   *
   * @param product user selected product
   * @return list of recommended products
   */
    public List<Product> getRecommendedProducts(Product product) {
      String url = "http://" + recommendationServiceUrl + ":" + recommendationServicePort + "/recommendations?product_id=" + product.getId();
      try {
          ResponseEntity<Product[]> response = restTemplate.getForEntity(url, Product[].class);
          if (response.getStatusCode() == HttpStatus.OK) {
              Product[] recommendedProducts = response.getBody();
              List<Product> validRecommendedProducts = new ArrayList<>();
              for (Product recommendedProduct : recommendedProducts) {
                  if (productService.findProductById(recommendedProduct.getId()).isPresent()) {
                      validRecommendedProducts.add(recommendedProduct);
                  }
              }
              return validRecommendedProducts;
          } else {
              return Collections.emptyList();
          }
      } catch (RestClientException e) {
          return Collections.emptyList();
      }
  }
}
