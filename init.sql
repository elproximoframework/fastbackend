CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    type VARCHAR,
    country VARCHAR,
    "countryName" VARCHAR,
    city VARCHAR,
    coordinates JSON,
    employees INTEGER,
    website VARCHAR,
    logo VARCHAR,
    description TEXT,
    founded INTEGER,
    ceo VARCHAR,
    sector VARCHAR,
    tags JSON,
    "socialLinks" JSON,
    "keyPrograms" JSON,
    "fundingStage" VARCHAR,
    "totalFunding" VARCHAR,
    "stockTicker" VARCHAR
);

CREATE INDEX ix_companies_name ON companies (name);
CREATE INDEX ix_companies_id ON companies (id);

CREATE TABLE rockets (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    manufacturer_id INTEGER REFERENCES companies(id),
    country VARCHAR,
    height DOUBLE PRECISION,
    diameter DOUBLE PRECISION,
    stages INTEGER,
    fuel VARCHAR,
    "leoCapacity" DOUBLE PRECISION,
    "gtoCapacity" DOUBLE PRECISION,
    "firstFlight" DATE,
    "totalLaunches" INTEGER,
    "successRate" DOUBLE PRECISION,
    status VARCHAR,
    image VARCHAR,
    description TEXT,
    "costPerLaunch" DOUBLE PRECISION,
    reusable BOOLEAN
);

CREATE INDEX ix_rockets_name ON rockets (name);
CREATE INDEX ix_rockets_id ON rockets (id);

CREATE TABLE satellites (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    "noradId" VARCHAR,
    operator_id INTEGER REFERENCES companies(id),
    purpose VARCHAR,
    "launchDate" DATE,
    "orbitType" VARCHAR,
    altitude DOUBLE PRECISION,
    inclination DOUBLE PRECISION,
    description TEXT,
    image VARCHAR,
    "isFeatured" BOOLEAN DEFAULT FALSE,
    "funFact" TEXT
);

CREATE INDEX ix_satellites_name ON satellites (name);
CREATE INDEX ix_satellites_noradId ON satellites ("noradId");
CREATE INDEX ix_satellites_id ON satellites (id);

CREATE TABLE launches (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    rocket_id INTEGER REFERENCES rockets(id),
    provider_id INTEGER REFERENCES companies(id),
    net DATE,
    status VARCHAR,
    mission_description TEXT,
    mission_type VARCHAR,
    orbit_name VARCHAR,
    pad_name VARCHAR,
    pad_location VARCHAR,
    webcast_live BOOLEAN DEFAULT FALSE,
    image VARCHAR
);

CREATE INDEX ix_launches_name ON launches (name);
CREATE INDEX ix_launches_id ON launches (id);
