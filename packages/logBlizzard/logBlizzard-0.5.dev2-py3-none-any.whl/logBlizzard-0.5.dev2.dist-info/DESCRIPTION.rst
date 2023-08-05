The goal is to provide distributed logging aggregation points, initially for syslog with longer term plans for other on-box logs. Aggregation points can be implemented close to the logging source either on a network device or other 3rd party compute node. Logging can be segmented into clusters with a hierarchy in each cluster. Message back-up/availability is built into the cluster logging architecture. Message dedup is the function of the ‘search head’. Each cluster has its own northbound API front end as part of a search head to be integrated with other systems.


