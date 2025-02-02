DO $$
BEGIN
  IF NOT EXISTS(SELECT 1 FROM information_schema.columns
      WHERE table_name = 'car' AND column_name = 'name') THEN
    ALTER TABLE "car" ADD COLUMN "name" VARCHAR(50) NOT NULL;
  END IF;
END $$;
