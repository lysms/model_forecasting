"use client"
import { useEffect, useState } from 'react';
import { Chart } from 'chart.js';

export default function Home() {

  const [salesData, setSalesData] = useState(null);

  useEffect(() => {
    console.log("ehhlo");
    const fetchData = async () => {
      try {
        const response = await fetch('/forecast?categories=M01AB,M01AE,N02BA&frequency=monthly');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Fetched data:', data);
        setSalesData(data);
      } catch (error) {
        console.error('Fetching error:', error);
      }
    };

    fetchData();
  }, []);


  useEffect(() => {

    if (salesData) {
      // Assuming 'historical' and 'forecast' data are arrays of the same length
      Object.keys(salesData.historical).forEach((category) => {
        const ctx = document.getElementById(`chart-${category}`).getContext('2d');
        new Chart(ctx, {
          type: 'line',
          data: {
            labels: Array.from({ length: salesData.historical[category].length }).map((_, i) => i),
            datasets: [
              {
                label: `Historical Sales for ${category}`,
                data: salesData.historical[category],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                fill: false,
              },
              {
                label: `Forecasted Sales for ${category}`,
                data: salesData.forecast[category],
                borderColor: 'rgb(153, 102, 255)',
                borderDash: [5, 5],
                tension: 0.1,
                fill: false,
              }
            ],
          },
          options: {
            animation: {
              duration: 2000,
              easing: 'easeInOutQuart',
            },
            scales: {
              y: {
                beginAtZero: true,
              }
            }
          },
        });
      });
    }
  }, [salesData]);

  return (
    <div>
      {salesData && Object.keys(salesData.historical).map((category) => (
        <canvas id={`chart-${category}`} key={category}></canvas>
      ))}
    </div>
  );
}
