-- MIT License
-- Copyright (c) 2020 Balancer Labs, markus@balancer.finance

-- Transfers of Liquidity Mining Power
-- On Polygon, Liquidity Mining Power is equivalent to BPTs

select 
  contract_address as token_address,
  `from` as from_address,
  `to` as to_address,
  value,
  block_number,
  block_timestamp
FROM `blockchain-etl.polygon_balancer.V2_BalancerPoolToken_event_Transfer`