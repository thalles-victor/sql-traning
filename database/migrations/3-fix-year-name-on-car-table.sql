DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns
      WHERE table_name = 'car' AND column_name = 'yearn') THEN
    ALTER TABLE "car" RENAME COLUMN "yearn" TO "year";
  END IF;
END $$;