class MaintainerDefenseKit < Formula
  desc "Audit repository governance and GitHub Actions risk offline"
  homepage "https://github.com/thangldw/awesome-maintainer-defense"
  url "https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.1/maintainer-defense-kit.py"
  sha256 "731670a8926134eda2348b53a81a92b7dfff00771a03100ab322bb9415c950a0"
  license "MIT"

  depends_on "python@3.12"

  def install
    libexec.install "maintainer-defense-kit.py" => "maintainer-defense"
    bin.write_exec_script libexec/"maintainer-defense"
  end

  test do
    assert_match "auditor 1.1; kit 1.1", shell_output("#{bin}/maintainer-defense --version")
    assert_match "findings", shell_output("#{bin}/maintainer-defense audit #{testpath} --format summary")
  end
end
