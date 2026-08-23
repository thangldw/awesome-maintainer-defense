class MaintainerDefenseKit < Formula
  desc "Audit repository governance and GitHub Actions risk offline"
  homepage "https://github.com/thangldw/awesome-maintainer-defense"
  url "https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.1.0/maintainer-defense-kit.py"
  sha256 "0fae945f1c2b45fe4c8f21c00525f2c276783409b5eefaf106e289e39c4ca8b3"
  license "MIT"

  depends_on "python@3.12"

  def install
    libexec.install "maintainer-defense-kit.py" => "maintainer-defense"
    chmod 0755, libexec/"maintainer-defense"
    bin.write_exec_script libexec/"maintainer-defense"
  end

  test do
    assert_match "auditor 1.1.0; kit 1.1.0", shell_output("#{bin}/maintainer-defense --version")
    assert_match "findings", shell_output("#{bin}/maintainer-defense audit #{testpath} --format summary")
  end
end
