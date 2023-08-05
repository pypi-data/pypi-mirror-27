--CREATE SCHEMA
CREATE SCHEMA IF NOT EXISTS sch_chameleon;

--VIEWS
CREATE OR REPLACE VIEW sch_chameleon.v_version 
 AS
	SELECT '1.7'::TEXT t_version
;

--TYPES
CREATE TYPE sch_chameleon.en_src_status
	AS ENUM ('ready', 'initialising','initialised','stopped','running','error');

CREATE TYPE sch_chameleon.en_binlog_event 
	AS ENUM ('delete', 'update', 'insert','ddl');

--TABLES/INDICES	
CREATE TABLE sch_chameleon.t_sources
(
	i_id_source	bigserial,
	t_source		text NOT NULL,
	t_source_schema   text ,
	t_dest_schema   text NOT NULL,
	enm_status sch_chameleon.en_src_status NOT NULL DEFAULT 'ready',
	ts_last_received timestamp without time zone,
	ts_last_replay timestamp without time zone,
	v_log_table character varying[] ,
	CONSTRAINT pk_t_sources PRIMARY KEY (i_id_source)
)
;

CREATE UNIQUE INDEX idx_t_sources_t_source ON sch_chameleon.t_sources(t_source);
CREATE UNIQUE INDEX idx_t_sources_t_dest_schema ON sch_chameleon.t_sources(t_dest_schema);


CREATE TABLE sch_chameleon.t_replica_batch
(
  i_id_batch bigserial NOT NULL,
  i_id_source bigint NOT NULL,
  t_binlog_name text,
  i_binlog_position integer,
  b_started boolean NOT NULL DEFAULT False,
  b_processed boolean NOT NULL DEFAULT False,
  b_replayed boolean NOT NULL DEFAULT False,
  ts_created timestamp without time zone NOT NULL DEFAULT clock_timestamp(),
  ts_processed timestamp without time zone ,
  ts_replayed timestamp without time zone ,
  i_replayed bigint NULL,
  i_skipped bigint NULL,
  i_ddl bigint NULL,
  CONSTRAINT pk_t_batch PRIMARY KEY (i_id_batch)
)
WITH (
  OIDS=FALSE
);

CREATE UNIQUE INDEX idx_t_replica_batch_binlog_name_position 
    ON sch_chameleon.t_replica_batch  (i_id_source,t_binlog_name,i_binlog_position);

CREATE UNIQUE INDEX idx_t_replica_batch_ts_created
	ON sch_chameleon.t_replica_batch (i_id_source,ts_created);

CREATE TABLE IF NOT EXISTS sch_chameleon.t_log_replica
(
  i_id_event bigserial NOT NULL,
  i_id_batch bigserial NOT NULL,
  v_table_name character varying(100) NOT NULL,
  v_schema_name character varying(100) NOT NULL,
  enm_binlog_event sch_chameleon.en_binlog_event NOT NULL,
  t_binlog_name text,
  i_binlog_position integer,
  ts_event_datetime timestamp without time zone NOT NULL DEFAULT clock_timestamp(),
  jsb_event_data jsonb,
  jsb_event_update jsonb,
  t_query text,
  i_my_event_time bigint,
  CONSTRAINT pk_log_replica PRIMARY KEY (i_id_event),
  CONSTRAINT fk_replica_batch FOREIGN KEY (i_id_batch) 
	REFERENCES  sch_chameleon.t_replica_batch (i_id_batch)
	ON UPDATE RESTRICT ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);


CREATE TABLE sch_chameleon.t_replica_tables
(
  i_id_table bigserial NOT NULL,
  i_id_source bigint NOT NULL,
  v_table_name character varying(100) NOT NULL,
  v_schema_name character varying(100) NOT NULL,
  v_table_pkey character varying(100)[] NOT NULL,
  t_binlog_name text,
  i_binlog_position integer,
  CONSTRAINT pk_t_replica_tables PRIMARY KEY (i_id_table)
)
WITH (
  OIDS=FALSE
);

CREATE UNIQUE INDEX idx_t_replica_tables_table_schema
	ON sch_chameleon.t_replica_tables (i_id_source,v_table_name,v_schema_name);


CREATE TABLE sch_chameleon.t_discarded_rows
(
	i_id_row		bigserial,
	i_id_batch	bigint NOT NULL,
	ts_discard	timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
	t_row_data	text,
	CONSTRAINT pk_t_discarded_rows PRIMARY KEY (i_id_row)
)
;
	
	
ALTER TABLE sch_chameleon.t_replica_batch
	ADD CONSTRAINT fk_t_replica_batch_i_id_source FOREIGN KEY (i_id_source)
	REFERENCES sch_chameleon.t_sources (i_id_source)
	ON UPDATE RESTRICT ON DELETE CASCADE
	;

ALTER TABLE sch_chameleon.t_replica_tables
	ADD CONSTRAINT fk_t_replica_tables_i_id_source FOREIGN KEY (i_id_source)
	REFERENCES sch_chameleon.t_sources (i_id_source)
	ON UPDATE RESTRICT ON DELETE CASCADE
	;



CREATE TABLE sch_chameleon.t_index_def
(
  i_id_def bigserial NOT NULL,
  i_id_source bigint NOT NULL,
  v_schema character varying(100),
  v_table character varying(100),
  v_index character varying(100),
  t_create	text,
  t_drop	text,
  CONSTRAINT pk_t_index_def PRIMARY KEY (i_id_def)
)
WITH (
  OIDS=FALSE
);

CREATE UNIQUE INDEX idx_schema_table_source ON sch_chameleon.t_index_def(i_id_source,v_schema,v_table,v_index);


CREATE TABLE sch_chameleon.t_batch_events
(
	i_id_batch	bigint NOT NULL,
	I_id_event	bigint[] NOT NULL,
	CONSTRAINT pk_t_batch_id_events PRIMARY KEY (i_id_batch)
)
;

ALTER TABLE sch_chameleon.t_batch_events
	ADD CONSTRAINT fk_t_batch_id_events_i_id_batch FOREIGN KEY (i_id_batch)
	REFERENCES sch_chameleon.t_replica_batch(i_id_batch)
	ON UPDATE RESTRICT ON DELETE CASCADE
	;

--FUNCTIONS
CREATE OR REPLACE FUNCTION sch_chameleon.fn_refresh_parts() 
RETURNS VOID as 
$BODY$
DECLARE
    t_sql text;
    r_tables record;
BEGIN
    FOR r_tables IN SELECT unnest(v_log_table) as v_log_table FROM sch_chameleon.t_sources
    LOOP
        RAISE DEBUG 'CREATING TABLE %', r_tables.v_log_table;
        t_sql:=format('
			CREATE TABLE IF NOT EXISTS sch_chameleon.%I
			(
			CONSTRAINT pk_%s PRIMARY KEY (i_id_event),
			  CONSTRAINT fk_%s FOREIGN KEY (i_id_batch) 
				REFERENCES  sch_chameleon.t_replica_batch (i_id_batch)
			ON UPDATE RESTRICT ON DELETE CASCADE
			)
			INHERITS (sch_chameleon.t_log_replica)
			;',
                        r_tables.v_log_table,
                        r_tables.v_log_table,
                        r_tables.v_log_table
                );
        EXECUTE t_sql;
	t_sql:=format('
			CREATE INDEX IF NOT EXISTS idx_id_batch_%s 
			ON sch_chameleon.%I (i_id_batch)
			;',
			r_tables.v_log_table,
                        r_tables.v_log_table
		);
	EXECUTE t_sql;
    END LOOP;
END
$BODY$
LANGUAGE plpgsql 
;

CREATE OR REPLACE FUNCTION sch_chameleon.fn_process_batch(integer,integer)
RETURNS BOOLEAN AS
$BODY$
	DECLARE
		p_i_max_events	ALIAS FOR $1;
		p_i_source_id		ALIAS FOR $2;
		v_b_loop		boolean;
		v_r_rows		record;
		v_i_id_batch		bigint;
		v_t_ddl		text;
		v_i_replayed		integer;
		v_i_skipped		integer;
		v_i_ddl		integer;
		v_i_evt_replay	bigint[];
		v_i_evt_queue		bigint[];
		v_ts_evt_source	timestamp without time zone;
	BEGIN
		v_b_loop:=FALSE;
		v_i_replayed:=0;
		v_i_ddl:=0;
		v_i_skipped:=0;
		
		
		v_i_id_batch:= (
			SELECT 
				bat.i_id_batch 
			FROM 
				sch_chameleon.t_replica_batch bat
				INNER JOIN  sch_chameleon.t_batch_events evt
				ON
					evt.i_id_batch=bat.i_id_batch
			WHERE 
					bat.b_started 
				AND	bat.b_processed 
				AND	NOT bat.b_replayed
				AND	bat.i_id_source=p_i_source_id
			ORDER BY 
				bat.ts_created 
			LIMIT 1
			)
		;

		v_i_evt_replay:=(
			SELECT 
				i_id_event[1:p_i_max_events] 
			FROM 
				sch_chameleon.t_batch_events 
			WHERE 
				i_id_batch=v_i_id_batch
		);
		
		
		v_i_evt_queue:=(
			SELECT 
				i_id_event[p_i_max_events+1:array_length(i_id_event,1)] 
			FROM 
				sch_chameleon.t_batch_events 
			WHERE 
				i_id_batch=v_i_id_batch
		);

		v_ts_evt_source:=(
			SELECT 
				to_timestamp(i_my_event_time)
			FROM	
				sch_chameleon.t_log_replica
			WHERE
					i_id_event=v_i_evt_replay[array_length(v_i_evt_replay,1)]
				AND	i_id_batch=v_i_id_batch
		);
		
		
		IF v_i_id_batch IS NULL 
		THEN
			RETURN v_b_loop;
		END IF;
		RAISE DEBUG 'Found id_batch %', v_i_id_batch;
		
		FOR v_r_rows IN 
			SELECT 
				CASE
					WHEN enm_binlog_event = 'ddl'
					THEN 
						t_query
					WHEN enm_binlog_event = 'insert'
					THEN
						format(
							'INSERT INTO %I.%I (%s) VALUES (%s);',
							v_schema_name,
							v_table_name,
							array_to_string(t_colunm,','),
							array_to_string(t_event_data,',')
							
						)
					WHEN enm_binlog_event = 'update'
					THEN
						format(
							'UPDATE %I.%I SET %s WHERE %s;',
							v_schema_name,
							v_table_name,
							t_update,
							t_pk_update
						)
					WHEN enm_binlog_event = 'delete'
					THEN
						format(
							'DELETE FROM %I.%I WHERE %s;',
							v_schema_name,
							v_table_name,
							t_pk_data
						)
					
				END AS t_sql,
				i_id_event,
				i_id_batch,
				enm_binlog_event
			FROM
			(
				SELECT
					i_id_event,
					i_id_batch,
					v_table_name,
					v_schema_name,
					enm_binlog_event,
					t_query,
					ts_event_datetime,
					t_pk_data,
					t_pk_update,
					array_agg(quote_ident(t_column)) AS t_colunm,
					string_agg(distinct format('%I=%L',t_column,jsb_event_data->>t_column),',') as  t_update,
					array_agg(quote_nullable(jsb_event_data->>t_column)) as t_event_data
				FROM
				(
					SELECT
						i_id_event,
						i_id_batch,
						v_table_name,
						v_schema_name,
						enm_binlog_event,
						jsb_event_data,
						jsb_event_update,
						t_query,
						ts_event_datetime,
						string_agg(distinct format('%I=%L',v_pkey,jsb_event_data->>v_pkey),' AND ') as  t_pk_data,
						string_agg(distinct format('%I=%L',v_pkey,jsb_event_update->>v_pkey),' AND ') as  t_pk_update,
						(jsonb_each_text(coalesce(jsb_event_data,'{"foo":"bar"}'::jsonb))).key AS t_column
					FROM
					(
						SELECT 
							i_id_event,
							i_id_batch,
							v_table_name,
							v_schema_name,
							enm_binlog_event,
							jsb_event_data,
							jsb_event_update,
							t_query,
							ts_event_datetime,
							replace(unnest(string_to_array(v_table_pkey[1],',')),'"','') as v_pkey
							
							
							
						FROM 
							(
								SELECT 
									log.i_id_event,
									log.i_id_batch,
									log.v_table_name,
									log.v_schema_name,
									log.enm_binlog_event,
									log.jsb_event_data,
									log.jsb_event_update,
									log.t_query,
									ts_event_datetime,
									v_table_pkey
									
									
									
								FROM 
									sch_chameleon.t_log_replica  log
									INNER JOIN sch_chameleon.t_replica_tables tab
										ON
												tab.v_table_name=log.v_table_name
											AND	tab.v_schema_name=log.v_schema_name
								WHERE
										log.i_id_batch=v_i_id_batch
									AND 	log.i_id_event=ANY(v_i_evt_replay) 
								
							) t_log
							
					) t_pkey
					GROUP BY
						i_id_event,
						i_id_batch,
						v_table_name,
						v_schema_name,
						enm_binlog_event,
						jsb_event_data,
						jsb_event_update,
						t_query,
						ts_event_datetime
				) t_columns
				GROUP BY
					i_id_event,
					i_id_batch,
					v_table_name,
					v_schema_name,
					enm_binlog_event,
					t_query,
					ts_event_datetime,
					t_pk_data,
					t_pk_update
			) t_sql
		ORDER BY i_id_event
		LOOP 	
			EXECUTE  v_r_rows.t_sql;
			IF v_r_rows.enm_binlog_event='ddl'
			THEN
				v_i_ddl:=v_i_ddl+1;
			ELSE
				v_i_replayed:=v_i_replayed+1;
			END IF;
			
			
			
			
		END LOOP;
		
		IF v_ts_evt_source IS NOT NULL
		THEN
			UPDATE sch_chameleon.t_sources 
				SET
					ts_last_replay=v_ts_evt_source
			WHERE 	
				i_id_source=p_i_source_id
			;
		END IF;
		IF v_i_replayed=0 AND v_i_ddl=0
		THEN
			DELETE FROM sch_chameleon.t_log_replica
			WHERE
    			    i_id_batch=v_i_id_batch
			;
				
			GET DIAGNOSTICS v_i_skipped = ROW_COUNT;

			UPDATE ONLY sch_chameleon.t_replica_batch  
			SET 
				b_replayed=True,
				i_skipped=v_i_skipped,
				ts_replayed=clock_timestamp()
				
			WHERE
				i_id_batch=v_i_id_batch
			;

			DELETE FROM sch_chameleon.t_batch_events
			WHERE
				i_id_batch=v_i_id_batch
			;

			v_b_loop=False;
		ELSE
			UPDATE ONLY sch_chameleon.t_replica_batch  
			SET 
				i_ddl=coalesce(i_ddl,0)+v_i_ddl,
				i_replayed=coalesce(i_replayed,0)+v_i_replayed,
				i_skipped=v_i_skipped,
				ts_replayed=clock_timestamp()
				
			WHERE
				i_id_batch=v_i_id_batch
			;

			UPDATE sch_chameleon.t_batch_events
				SET
					i_id_event = v_i_evt_queue
			WHERE
				i_id_batch=v_i_id_batch
			;

			DELETE FROM sch_chameleon.t_log_replica
			WHERE
					i_id_batch=v_i_id_batch
				AND 	i_id_event=ANY(v_i_evt_replay) 
			;
			
			v_b_loop=True;


			
		END IF;
		
		v_i_id_batch:= (
			SELECT 
				bat.i_id_batch 
			FROM 
				sch_chameleon.t_replica_batch bat
				INNER JOIN  sch_chameleon.t_batch_events evt
				ON
					evt.i_id_batch=bat.i_id_batch
			WHERE 
					bat.b_started 
				AND	bat.b_processed 
				AND	NOT bat.b_replayed
				AND	bat.i_id_source=p_i_source_id
			ORDER BY 
				bat.ts_created 
			LIMIT 1
			)
		;
		
		IF v_i_id_batch IS NOT NULL
		THEN
			v_b_loop=True;
		END IF;
		
		
		RETURN v_b_loop;

	
	END;
$BODY$
LANGUAGE plpgsql;
